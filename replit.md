# FoodWasteReducer - Food Redistribution Platform

## Overview

FoodWasteReducer is a web-based platform designed to connect restaurants, citizens, NGOs, and drivers to reduce food waste and fight hunger in communities. The application facilitates the donation, claiming, and delivery of surplus food through a role-based system where different user types can contribute to the food redistribution ecosystem.

The platform enables restaurants and citizens to donate surplus food, NGOs to claim donations for distribution, and drivers to facilitate delivery logistics. It includes user authentication, donation management, impact tracking, and a dashboard interface tailored to each user role.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap with dark theme for responsive design
- **Icons**: Feather Icons for consistent iconography
- **Charts**: Chart.js for data visualization and impact metrics
- **Forms**: Flask-WTF with WTForms for form handling and validation

### Backend Architecture
- **Web Framework**: Flask with modular route organization
- **Authentication**: Flask-Login for session management and user authentication
- **Security**: Werkzeug for password hashing and CSRF protection via Flask-WTF
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Data Storage
- **Current Implementation**: In-memory storage using Python dictionaries for MVP
- **Storage Modules**: Centralized storage layer in `storage.py` for easy database migration
- **Data Models**: Object-oriented models for Users and Donations with UUID-based identifiers
- **Statistics**: Real-time calculation of platform metrics from stored data

### User Management System
- **Role-Based Access**: Four distinct user roles (restaurant, citizen, ngo, driver)
- **User Model**: UserMixin integration for Flask-Login compatibility
- **Password Security**: Werkzeug password hashing with salt
- **User Lookup**: Multiple lookup methods (ID, username, email)

### Application Structure
- **Modular Design**: Separation of concerns across multiple files (routes, models, forms, storage)
- **Route Organization**: Centralized routing in `routes.py` with role-based access control
- **Form Validation**: Comprehensive form validation with custom validators
- **Error Handling**: Flash messaging system for user feedback

## External Dependencies

### Python Packages
- **Flask**: Core web framework
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Werkzeug**: WSGI utilities and security functions

### Frontend Dependencies
- **Bootstrap CSS**: UI framework with Replit dark theme
- **Chart.js**: Data visualization library
- **Feather Icons**: Icon library for UI elements

### Development Tools
- **Python Logging**: Built-in logging for debugging and monitoring
- **Werkzeug ProxyFix**: Middleware for reverse proxy deployment

### Future Database Integration
The current in-memory storage system is designed for easy migration to a persistent database solution. The storage layer abstraction allows for seamless integration with SQL databases or ORMs like SQLAlchemy without requiring changes to the model or route logic.