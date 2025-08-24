from flask import Blueprint, render_template

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctor')
def doctor_list():
    doctors = [
        {
            'id': 1,
            'name': 'Dr. Sarah Johnson',
            'specialty': 'Cardiologist',
            'experience': 15,
            'rating': 4.8,
            'image': 'doctor1.jpg',
            'location': 'New York, NY',
            'bio': 'Specialized in heart disease prevention and treatment.'
        },
        {
            'id': 2,
            'name': 'Dr. Michael Chen',
            'specialty': 'Neurologist',
            'experience': 12,
            'rating': 4.9,
            'image': 'doctor2.jpg',
            'location': 'Los Angeles, CA',
            'bio': 'Expert in brain and nervous system disorders.'
        },
        {
            'id': 3,
            'name': 'Dr. Emily Rodriguez',
            'specialty': 'Pediatrician',
            'experience': 8,
            'rating': 4.7,
            'image': 'doctor3.jpg',
            'location': 'Chicago, IL',
            'bio': 'Dedicated to children\'s health and wellness.'
        },
        {
            'id': 4,
            'name': 'Dr. David Wilson',
            'specialty': 'Orthopedic Surgeon',
            'experience': 20,
            'rating': 4.6,
            'image': 'doctor4.jpg',
            'location': 'Houston, TX',
            'bio': 'Specialist in bone and joint surgery.'
        },
        {
            'id': 5,
            'name': 'Dr. Lisa Thompson',
            'specialty': 'Dermatologist',
            'experience': 10,
            'rating': 4.5,
            'image': 'doctor5.jpg',
            'location': 'Miami, FL',
            'bio': 'Expert in skin conditions and cosmetic procedures.'
        },
        {
            'id': 6,
            'name': 'Dr. Robert Kim',
            'specialty': 'Psychiatrist',
            'experience': 18,
            'rating': 4.9,
            'image': 'doctor6.jpg',
            'location': 'Seattle, WA',
            'bio': 'Specializes in mental health and behavioral disorders.'
        }
        # Add more doctors as needed to reach ~20 total
    ]
    return render_template("doctor.html", doctors=doctors)
