from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from models import User, Donation
from forms import LoginForm, RegistrationForm, DonationForm
from storage import get_statistics
import logging

@app.route('/')
def index():
    """Home page"""
    stats = get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.get_by_username(form.username.data):
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        if User.get_by_email(form.email.data):
            flash('Email already registered. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        password_hash = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash,
            role=form.role.data,
            name=form.name.data,
            phone=form.phone.data
        )
        user.save()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard"""
    if current_user.role in ['restaurant', 'citizen']:
        # Show user's donations
        user_donations = Donation.get_by_donor(current_user.id)
        return render_template('dashboard.html', donations=user_donations)
    
    elif current_user.role == 'ngo':
        # Show available donations and claimed donations
        available_donations = Donation.get_by_status('Pending')
        claimed_donations = Donation.get_by_ngo(current_user.id)
        return render_template('dashboard.html', 
                             available_donations=available_donations,
                             claimed_donations=claimed_donations)
    
    elif current_user.role == 'driver':
        # Show assigned deliveries
        assigned_deliveries = Donation.get_by_driver(current_user.id)
        # Show claimed donations that need drivers
        available_deliveries = [d for d in Donation.get_by_status('Claimed') if not d.driver_id]
        return render_template('dashboard.html',
                             assigned_deliveries=assigned_deliveries,
                             available_deliveries=available_deliveries)
    
    return render_template('dashboard.html')

@app.route('/add_donation', methods=['GET', 'POST'])
@login_required
def add_donation():
    """Add food donation (for restaurants and citizens)"""
    if current_user.role not in ['restaurant', 'citizen']:
        flash('Only restaurants and citizens can add donations.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            donor_id=current_user.id,
            donor_name=current_user.name,
            food_type=form.food_type.data,
            quantity=form.quantity.data,
            description=form.description.data,
            location=form.location.data,
            contact_phone=form.contact_phone.data
        )
        donation.save()
        
        flash('Donation added successfully! NGOs can now view and claim it.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_donation.html', form=form)

@app.route('/view_donations')
@login_required
def view_donations():
    """View available donations (for NGOs)"""
    if current_user.role != 'ngo':
        flash('Only NGOs can view available donations.', 'danger')
        return redirect(url_for('dashboard'))
    
    available_donations = Donation.get_by_status('Pending')
    return render_template('view_donations.html', donations=available_donations)

@app.route('/claim_donation/<donation_id>')
@login_required
def claim_donation(donation_id):
    """Claim a donation (for NGOs)"""
    if current_user.role != 'ngo':
        flash('Only NGOs can claim donations.', 'danger')
        return redirect(url_for('dashboard'))
    
    donation = Donation.get(donation_id)
    if not donation:
        flash('Donation not found.', 'danger')
        return redirect(url_for('view_donations'))
    
    if donation.claim(current_user.id, current_user.name):
        flash('Donation claimed successfully!', 'success')
    else:
        flash('Donation could not be claimed. It may have already been claimed.', 'warning')
    
    return redirect(url_for('dashboard'))

@app.route('/assign_driver/<donation_id>')
@login_required
def assign_driver(donation_id):
    """Assign driver to delivery (for drivers)"""
    if current_user.role != 'driver':
        flash('Only drivers can assign themselves to deliveries.', 'danger')
        return redirect(url_for('dashboard'))
    
    donation = Donation.get(donation_id)
    if not donation:
        flash('Donation not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    if donation.assign_driver(current_user.id, current_user.name):
        flash('You have been assigned to this delivery!', 'success')
    else:
        flash('Could not assign to this delivery. It may not be available.', 'warning')
    
    return redirect(url_for('dashboard'))

@app.route('/mark_delivered/<donation_id>')
@login_required
def mark_delivered(donation_id):
    """Mark donation as delivered (for drivers)"""
    if current_user.role != 'driver':
        flash('Only drivers can mark deliveries as completed.', 'danger')
        return redirect(url_for('dashboard'))
    
    donation = Donation.get(donation_id)
    if not donation:
        flash('Donation not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    if donation.driver_id != current_user.id:
        flash('You can only mark your own assigned deliveries as completed.', 'danger')
        return redirect(url_for('dashboard'))
    
    if donation.mark_delivered():
        flash('Delivery marked as completed! Thank you for your service.', 'success')
    else:
        flash('Could not mark delivery as completed.', 'warning')
    
    return redirect(url_for('dashboard'))

@app.route('/impact')
@login_required
def impact():
    """Impact tracking page with analytics"""
    stats = get_statistics()
    
    # Get user-specific stats
    if current_user.role in ['restaurant', 'citizen']:
        user_donations = Donation.get_by_donor(current_user.id)
        user_stats = {
            'total_donations': len(user_donations),
            'delivered_donations': len([d for d in user_donations if d.status == 'Delivered']),
            'pending_donations': len([d for d in user_donations if d.status == 'Pending']),
            'claimed_donations': len([d for d in user_donations if d.status == 'Claimed'])
        }
    elif current_user.role == 'ngo':
        ngo_donations = Donation.get_by_ngo(current_user.id)
        user_stats = {
            'total_claimed': len(ngo_donations),
            'delivered_donations': len([d for d in ngo_donations if d.status == 'Delivered']),
            'pending_deliveries': len([d for d in ngo_donations if d.status == 'Claimed'])
        }
    elif current_user.role == 'driver':
        driver_deliveries = Donation.get_by_driver(current_user.id)
        user_stats = {
            'total_deliveries': len(driver_deliveries),
            'completed_deliveries': len([d for d in driver_deliveries if d.status == 'Delivered']),
            'pending_deliveries': len([d for d in driver_deliveries if d.status == 'Claimed'])
        }
    else:
        user_stats = {}
    
    return render_template('impact.html', stats=stats, user_stats=user_stats)

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for chart data"""
    stats = get_statistics()
    return jsonify(stats)
