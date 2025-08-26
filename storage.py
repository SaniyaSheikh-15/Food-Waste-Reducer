"""
In-memory storage for the MVP version
In production, this would be replaced with a proper database
"""

# Dictionary to store users (key: user_id, value: User object)
users = {}

# Dictionary to store donations (key: donation_id, value: Donation object)
donations = {}

def get_statistics():
    """Get platform statistics"""
    total_donations = len(donations)
    pending_donations = len([d for d in donations.values() if d.status == 'Pending'])
    claimed_donations = len([d for d in donations.values() if d.status == 'Claimed'])
    delivered_donations = len([d for d in donations.values() if d.status == 'Delivered'])
    
    total_users = len(users)
    restaurants = len([u for u in users.values() if u.role == 'restaurant'])
    citizens = len([u for u in users.values() if u.role == 'citizen'])
    ngos = len([u for u in users.values() if u.role == 'ngo'])
    drivers = len([u for u in users.values() if u.role == 'driver'])
    
    return {
        'total_donations': total_donations,
        'pending_donations': pending_donations,
        'claimed_donations': claimed_donations,
        'delivered_donations': delivered_donations,
        'total_users': total_users,
        'restaurants': restaurants,
        'citizens': citizens,
        'ngos': ngos,
        'drivers': drivers
    }
