import streamlit as st
import requests
import pandas as pd
import random
from datetime import datetime, timedelta
import time
import json
import urllib.parse


# ── Language strings ─────────────────────────────────────────────────────────
LANG = {
    "English": {
        "app_title": "Driver AI Copilot",
        "tagline": "Smart Decisions. Higher Earnings.",
        "login_title": "Welcome, Driver!",
        "login_name": "Full Name",
        "login_phone": "Phone Number",
        "login_vehicle": "Vehicle Number",
        "login_btn": "Start Driving",
        "nav_dashboard": "Dashboard",
        "nav_heatmap": "Heatmap",
        "nav_earnings": "Earnings",
        "nav_recommend": "Recommendations",
        "nav_history": "Ride History",
        "nav_assistant": "AI Assistant",
        "nav_fuel": "Fuel & Expenses",
        "nav_maintenance": "Maintenance",
        "nav_safety": "Safety & SOS",
        "nav_settings": "Settings",
        "nav_logout": "Logout",
        "today_earn": "Today's Earnings",
        "exp_earn": "Expected (Next 1 Hr)",
        "demand_score": "Demand Score",
        "idle_time": "Idle Time",
        "acceptance": "Acceptance Rate",
        "live_heatmap": "Live Demand Heatmap",
        "ai_rec": "AI Recommendation",
        "best_option": "Best Option",
        "move_to": "Move to",
        "exp_earnings": "Expected Earnings",
        "distance": "Distance",
        "demand": "Demand",
        "idle_reduction": "Idle Time Reduction",
        "get_directions": "Open in Google Maps →",
        "earn_predict": "Earnings — Next 4 Hours",
        "top_zones": "Top Demand Zones (Next 1 Hour)",
        "recent_rides": "Recent Rides",
        "view_all": "View All Rides →",
        "ai_assistant": "AI Assistant",
        "ask_placeholder": "Ask me anything about your ride, earnings, zones...",
        "very_high": "Very High",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "active_driver": "Active Driver",
        "total_rides": "Total Rides",
        "total_earn": "Total Earnings",
        "online_hours": "Online Hours",
        "vs_yesterday": "vs yesterday",
        "high_demand": "High demand expected",
        "navigate_now": "Navigate Now",
        "logout_confirm": "Logged out successfully!",
        "online": "Live",
        "thinking": "Thinking...",
        "clear_chat": "Clear Chat",
        "powered_by": "Powered by Claude AI",
        "rides_today": "Rides Today",
        "bonus_progress": "Bonus Progress",
        "rides_to_bonus": "rides to ₹150 bonus!",
        "streak": "Day Streak 🔥",
        "tip_of_day": "💡 Tip",
        "navigate_zone": "Navigate to Zone",
        "current_hour": "Now",
        "earnings_bar": "Earnings Comparison",
        # Fuel
        "fuel_title": "Fuel & Expense Tracker",
        "add_fuel": "Log Fuel Fill-Up",
        "fuel_date": "Date",
        "fuel_liters": "Liters Filled",
        "fuel_cost": "Total Cost (₹)",
        "fuel_odometer": "Odometer (km)",
        "fuel_save": "Save Entry",
        "fuel_history": "Fuel Log History",
        "fuel_stats": "Fuel Statistics",
        "avg_mileage": "Avg Mileage",
        "total_fuel_cost": "Total Fuel Spend",
        "fuel_per_km": "Fuel Cost / km",
        "expense_title": "Other Expenses",
        "add_expense": "Log Expense",
        "expense_type": "Expense Type",
        "expense_amount": "Amount (₹)",
        "expense_note": "Note",
        "expense_save": "Add Expense",
        "profit_loss": "Profit / Loss Summary",
        # Maintenance
        "maint_title": "Vehicle Maintenance",
        "maint_schedule": "Maintenance Schedule",
        "maint_log": "Service Log",
        "add_service": "Log Service",
        "service_type": "Service Type",
        "service_date": "Service Date",
        "service_cost": "Cost (₹)",
        "service_notes": "Notes",
        "service_save": "Save Service",
        "next_service": "Next Service Due",
        "maint_reminders": "Reminders",
        "maint_history": "Service History",
        "vehicle_health": "Vehicle Health Score",
        "overdue": "Overdue",
        "due_soon": "Due Soon",
        "good": "Good",
        # Safety
        "safety_title": "Safety & SOS",
        "sos_title": "Emergency SOS",
        "sos_desc": "In danger? Press SOS to alert contacts + platform immediately.",
        "sos_btn": "🚨 SEND SOS ALERT",
        "sos_sent": "🚨 SOS SENT! Help is on the way.",
        "safety_contacts": "Emergency Contacts",
        "add_contact": "Add Emergency Contact",
        "contact_name": "Name",
        "contact_phone": "Phone",
        "contact_relation": "Relation",
        "contact_save": "Save Contact",
        "live_location": "Live Location Sharing",
        "share_with": "Sharing with",
        "safety_checklist": "Daily Safety Checklist",
        "incident_report": "Report an Incident",
        "incident_type": "Incident Type",
        "incident_desc": "Description",
        "incident_zone": "Zone where it happened",
        "incident_time": "Time of Incident",
        "incident_submit": "Submit Report",
        "safety_score": "Safety Score",
        "safe_zones": "Safe Zone Alerts",
        "night_mode": "Night Safety Mode",
        "night_mode_desc": "Auto-share location every 30 mins after 10 PM",
        "checkin_btn": "✅ I'm Safe — Check In",
        "last_checkin": "Last check-in",
    },
    "தமிழ்": {
        "app_title": "டிரைவர் AI கோபைலட்",
        "tagline": "சரியான முடிவுகள். அதிக வருமானம்.",
        "login_title": "வணக்கம், டிரைவர்!",
        "login_name": "முழு பெயர்",
        "login_phone": "தொலைபேசி எண்",
        "login_vehicle": "வாகன எண்",
        "login_btn": "ஓட்டுதல் தொடங்கு",
        "nav_dashboard": "டாஷ்போர்டு",
        "nav_heatmap": "தேவை வரைபடம்",
        "nav_earnings": "வருமானம்",
        "nav_recommend": "பரிந்துரைகள்",
        "nav_history": "பயண வரலாறு",
        "nav_assistant": "AI உதவியாளர்",
        "nav_fuel": "எரிபொருள் & செலவு",
        "nav_maintenance": "பராமரிப்பு",
        "nav_safety": "பாதுகாப்பு & SOS",
        "nav_settings": "அமைப்புகள்",
        "nav_logout": "வெளியேறு",
        "today_earn": "இன்றைய வருமானம்",
        "exp_earn": "எதிர்பார்க்கப்படும் (அடுத்த 1 மணி)",
        "demand_score": "தேவை மதிப்பெண்",
        "idle_time": "காத்திருப்பு நேரம்",
        "acceptance": "ஏற்பு விகிதம்",
        "live_heatmap": "நேரடி தேவை வரைபடம்",
        "ai_rec": "AI பரிந்துரை",
        "best_option": "சிறந்த விருப்பம்",
        "move_to": "செல்லுங்கள்",
        "exp_earnings": "எதிர்பார்க்கப்படும் வருமானம்",
        "distance": "தூரம்",
        "demand": "தேவை",
        "idle_reduction": "காத்திருப்பு குறைப்பு",
        "get_directions": "Google Maps திற →",
        "earn_predict": "வருமானம் — அடுத்த 4 மணி",
        "top_zones": "சிறந்த தேவை பகுதிகள்",
        "recent_rides": "சமீபத்திய பயணங்கள்",
        "view_all": "அனைத்து பயணங்களும் →",
        "ai_assistant": "AI உதவியாளர்",
        "ask_placeholder": "எதையும் கேளுங்கள்...",
        "very_high": "மிக அதிகம்",
        "high": "அதிகம்",
        "medium": "நடுத்தரம்",
        "low": "குறைவு",
        "active_driver": "செயலில் உள்ள டிரைவர்",
        "total_rides": "மொத்த பயணங்கள்",
        "total_earn": "மொத்த வருமானம்",
        "online_hours": "ஆன்லைன் நேரம்",
        "vs_yesterday": "நேற்றை விட",
        "high_demand": "அதிக தேவை எதிர்பார்க்கப்படுகிறது",
        "navigate_now": "இப்போது செல்",
        "logout_confirm": "வெற்றிகரமாக வெளியேறினீர்கள்!",
        "online": "நேரடி",
        "thinking": "யோசிக்கிறேன்...",
        "clear_chat": "அழி",
        "powered_by": "Claude AI மூலம்",
        "rides_today": "இன்று பயணங்கள்",
        "bonus_progress": "போனஸ் நிலை",
        "rides_to_bonus": "பயணங்கள் ₹150 போனஸ்!",
        "streak": "தொடர் நாட்கள் 🔥",
        "tip_of_day": "💡 டிப்ஸ்",
        "navigate_zone": "Zone-க்கு செல்",
        "current_hour": "இப்போது",
        "earnings_bar": "வருமான ஒப்பீடு",
        "fuel_title": "எரிபொருள் & செலவு",
        "add_fuel": "எரிபொருள் பதிவு",
        "fuel_date": "தேதி",
        "fuel_liters": "லிட்டர்",
        "fuel_cost": "செலவு (₹)",
        "fuel_odometer": "ஓடோமீட்டர் (km)",
        "fuel_save": "சேமி",
        "fuel_history": "எரிபொருள் வரலாறு",
        "fuel_stats": "புள்ளிவிவரங்கள்",
        "avg_mileage": "சராசரி மைலேஜ்",
        "total_fuel_cost": "மொத்த எரிபொருள் செலவு",
        "fuel_per_km": "கி.மீ செலவு",
        "expense_title": "பிற செலவுகள்",
        "add_expense": "செலவு பதிவு",
        "expense_type": "வகை",
        "expense_amount": "தொகை (₹)",
        "expense_note": "குறிப்பு",
        "expense_save": "சேமி",
        "profit_loss": "லாப / நஷ்ட சுருக்கம்",
        "maint_title": "வாகன பராமரிப்பு",
        "maint_schedule": "பராமரிப்பு அட்டவணை",
        "maint_log": "சேவை பதிவு",
        "add_service": "சேவை சேர்",
        "service_type": "சேவை வகை",
        "service_date": "தேதி",
        "service_cost": "செலவு (₹)",
        "service_notes": "குறிப்புகள்",
        "service_save": "சேமி",
        "next_service": "அடுத்த சேவை",
        "maint_reminders": "நினைவூட்டல்கள்",
        "maint_history": "சேவை வரலாறு",
        "vehicle_health": "வாகன நலன் மதிப்பெண்",
        "overdue": "தாமதம்",
        "due_soon": "விரைவில்",
        "good": "சரி",
        "safety_title": "பாதுகாப்பு & SOS",
        "sos_title": "அவசர SOS",
        "sos_desc": "ஆபத்தில் உள்ளீர்களா? SOS அழுத்தவும்.",
        "sos_btn": "🚨 SOS அனுப்பு",
        "sos_sent": "🚨 SOS அனுப்பப்பட்டது!",
        "safety_contacts": "அவசர தொடர்புகள்",
        "add_contact": "தொடர்பு சேர்",
        "contact_name": "பெயர்",
        "contact_phone": "தொலைபேசி",
        "contact_relation": "உறவு",
        "contact_save": "சேமி",
        "live_location": "நேரடி இருப்பிட பகிர்வு",
        "share_with": "பகிர்வு",
        "safety_checklist": "தினசரி பாதுகாப்பு சோதனை",
        "incident_report": "சம்பவம் புகார்",
        "incident_type": "சம்பவ வகை",
        "incident_desc": "விளக்கம்",
        "incident_zone": "Zone",
        "incident_time": "நேரம்",
        "incident_submit": "சமர்ப்பி",
        "safety_score": "பாதுகாப்பு மதிப்பெண்",
        "safe_zones": "பாதுகாப்பான பகுதி",
        "night_mode": "இரவு பாதுகாப்பு",
        "night_mode_desc": "இரவு 10 மணிக்கு பிறகு 30 நிமிடம் இடம் பகிரவும்",
        "checkin_btn": "✅ நான் பாதுகாப்பாக இருக்கிறேன்",
        "last_checkin": "கடைசி check-in",
    },
    "हिंदी": {
        "app_title": "ड्राइवर AI कोपायलट",
        "tagline": "सही निर्णय। अधिक कमाई।",
        "login_title": "स्वागत है, ड्राइवर!",
        "login_name": "पूरा नाम",
        "login_phone": "फोन नंबर",
        "login_vehicle": "वाहन नंबर",
        "login_btn": "ड्राइविंग शुरू करें",
        "nav_dashboard": "डैशबोर्ड",
        "nav_heatmap": "हीटमैप",
        "nav_earnings": "कमाई",
        "nav_recommend": "सिफारिशें",
        "nav_history": "राइड इतिहास",
        "nav_assistant": "AI सहायक",
        "nav_fuel": "ईंधन & खर्च",
        "nav_maintenance": "रखरखाव",
        "nav_safety": "सुरक्षा & SOS",
        "nav_settings": "सेटिंग्स",
        "nav_logout": "लॉगआउट",
        "today_earn": "आज की कमाई",
        "exp_earn": "अपेक्षित (अगला 1 घंटा)",
        "demand_score": "मांग स्कोर",
        "idle_time": "निष्क्रिय समय",
        "acceptance": "स्वीकृति दर",
        "live_heatmap": "लाइव डिमांड हीटमैप",
        "ai_rec": "AI सिफारिश",
        "best_option": "सबसे अच्छा",
        "move_to": "जाएं",
        "exp_earnings": "अपेक्षित कमाई",
        "distance": "दूरी",
        "demand": "मांग",
        "idle_reduction": "खाली समय कमी",
        "get_directions": "Google Maps खोलें →",
        "earn_predict": "कमाई — अगले 4 घंटे",
        "top_zones": "शीर्ष मांग क्षेत्र",
        "recent_rides": "हालिया राइड",
        "view_all": "सभी राइड →",
        "ai_assistant": "AI सहायक",
        "ask_placeholder": "कुछ भी पूछें...",
        "very_high": "बहुत अधिक",
        "high": "अधिक",
        "medium": "मध्यम",
        "low": "कम",
        "active_driver": "सक्रिय ड्राइवर",
        "total_rides": "कुल राइड",
        "total_earn": "कुल कमाई",
        "online_hours": "ऑनलाइन घंटे",
        "vs_yesterday": "कल की तुलना में",
        "high_demand": "उच्च मांग अपेक्षित",
        "navigate_now": "अभी जाएं",
        "logout_confirm": "सफलतापूर्वक लॉगआउट!",
        "online": "लाइव",
        "thinking": "सोच रहा हूं...",
        "clear_chat": "साफ करें",
        "powered_by": "Claude AI द्वारा",
        "rides_today": "आज की राइड",
        "bonus_progress": "बोनस प्रगति",
        "rides_to_bonus": "राइड ₹150 बोनस के लिए!",
        "streak": "दिन स्ट्रीक 🔥",
        "tip_of_day": "💡 सुझाव",
        "navigate_zone": "जोन पर जाएं",
        "current_hour": "अभी",
        "earnings_bar": "कमाई तुलना",
        "fuel_title": "ईंधन & खर्च ट्रैकर",
        "add_fuel": "ईंधन लॉग करें",
        "fuel_date": "तारीख",
        "fuel_liters": "लीटर",
        "fuel_cost": "कुल खर्च (₹)",
        "fuel_odometer": "ओडोमीटर (km)",
        "fuel_save": "सेव करें",
        "fuel_history": "ईंधन इतिहास",
        "fuel_stats": "आंकड़े",
        "avg_mileage": "औसत माइलेज",
        "total_fuel_cost": "कुल ईंधन खर्च",
        "fuel_per_km": "₹/किमी",
        "expense_title": "अन्य खर्च",
        "add_expense": "खर्च जोड़ें",
        "expense_type": "प्रकार",
        "expense_amount": "राशि (₹)",
        "expense_note": "नोट",
        "expense_save": "जोड़ें",
        "profit_loss": "लाभ / हानि",
        "maint_title": "वाहन रखरखाव",
        "maint_schedule": "रखरखाव अनुसूची",
        "maint_log": "सेवा लॉग",
        "add_service": "सेवा जोड़ें",
        "service_type": "सेवा प्रकार",
        "service_date": "तारीख",
        "service_cost": "खर्च (₹)",
        "service_notes": "नोट्स",
        "service_save": "सेव करें",
        "next_service": "अगली सेवा",
        "maint_reminders": "रिमाइंडर",
        "maint_history": "सेवा इतिहास",
        "vehicle_health": "वाहन स्वास्थ्य स्कोर",
        "overdue": "देरी",
        "due_soon": "जल्द",
        "good": "अच्छा",
        "safety_title": "सुरक्षा & SOS",
        "sos_title": "आपातकालीन SOS",
        "sos_desc": "खतरे में हैं? SOS दबाएं।",
        "sos_btn": "🚨 SOS भेजें",
        "sos_sent": "🚨 SOS भेजा गया!",
        "safety_contacts": "आपातकालीन संपर्क",
        "add_contact": "संपर्क जोड़ें",
        "contact_name": "नाम",
        "contact_phone": "फोन",
        "contact_relation": "संबंध",
        "contact_save": "सेव करें",
        "live_location": "लाइव लोकेशन शेयर",
        "share_with": "शेयर",
        "safety_checklist": "दैनिक सुरक्षा जांच",
        "incident_report": "घटना रिपोर्ट",
        "incident_type": "घटना प्रकार",
        "incident_desc": "विवरण",
        "incident_zone": "Zone",
        "incident_time": "समय",
        "incident_submit": "जमा करें",
        "safety_score": "सुरक्षा स्कोर",
        "safe_zones": "सुरक्षित क्षेत्र",
        "night_mode": "रात सुरक्षा मोड",
        "night_mode_desc": "रात 10 बजे के बाद हर 30 मिनट लोकेशन शेयर",
        "checkin_btn": "✅ मैं सुरक्षित हूं",
        "last_checkin": "अंतिम check-in",
    },
    "ಕನ್ನಡ": {
        "app_title": "ಡ್ರೈವರ್ AI ಕೋಪೈಲಟ್",
        "tagline": "ಸರಿಯಾದ ನಿರ್ಧಾರ. ಹೆಚ್ಚು ಆದಾಯ.",
        "login_title": "ಸ್ವಾಗತ, ಡ್ರೈವರ್!",
        "login_name": "ಪೂರ್ಣ ಹೆಸರು",
        "login_phone": "ಫೋನ್ ಸಂಖ್ಯೆ",
        "login_vehicle": "ವಾಹನ ಸಂಖ್ಯೆ",
        "login_btn": "ಡ್ರೈವಿಂಗ್ ಪ್ರಾರಂಭಿಸಿ",
        "nav_dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "nav_heatmap": "ಹೀಟ್‌ಮ್ಯಾಪ್",
        "nav_earnings": "ಆದಾಯ",
        "nav_recommend": "ಶಿಫಾರಸುಗಳು",
        "nav_history": "ರೈಡ್ ಇತಿಹಾಸ",
        "nav_assistant": "AI ಸಹಾಯಕ",
        "nav_fuel": "ಇಂಧನ & ಖರ್ಚು",
        "nav_maintenance": "ನಿರ್ವಹಣೆ",
        "nav_safety": "ಸುರಕ್ಷತೆ & SOS",
        "nav_settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "nav_logout": "ಲಾಗ್‌ಔಟ್",
        "today_earn": "ಇಂದಿನ ಆದಾಯ",
        "exp_earn": "ನಿರೀಕ್ಷಿತ (ಮುಂದಿನ 1 ಗಂಟೆ)",
        "demand_score": "ಬೇಡಿಕೆ ಸ್ಕೋರ್",
        "idle_time": "ನಿಷ್ಕ್ರಿಯ ಸಮಯ",
        "acceptance": "ಸ್ವೀಕೃತಿ ದರ",
        "live_heatmap": "ನೇರ ಬೇಡಿಕೆ ನಕ್ಷೆ",
        "ai_rec": "AI ಶಿಫಾರಸು",
        "best_option": "ಅತ್ಯುತ್ತಮ",
        "move_to": "ಹೋಗಿ",
        "exp_earnings": "ನಿರೀಕ್ಷಿತ ಆದಾಯ",
        "distance": "ದೂರ",
        "demand": "ಬೇಡಿಕೆ",
        "idle_reduction": "ನಿಷ್ಕ್ರಿಯ ಸಮಯ ಕಡಿತ",
        "get_directions": "Google Maps ತೆರೆಯಿರಿ →",
        "earn_predict": "ಆದಾಯ — ಮುಂದಿನ 4 ಗಂಟೆ",
        "top_zones": "ಉನ್ನತ ಬೇಡಿಕೆ ವಲಯಗಳು",
        "recent_rides": "ಇತ್ತೀಚಿನ ರೈಡ್‌ಗಳು",
        "view_all": "ಎಲ್ಲಾ ರೈಡ್‌ಗಳು →",
        "ai_assistant": "AI ಸಹಾಯಕ",
        "ask_placeholder": "ಏನಾದರೂ ಕೇಳಿ...",
        "very_high": "ತುಂಬಾ ಹೆಚ್ಚು",
        "high": "ಹೆಚ್ಚು",
        "medium": "ಮಧ್ಯಮ",
        "low": "ಕಡಿಮೆ",
        "active_driver": "ಸಕ್ರಿಯ ಡ್ರೈವರ್",
        "total_rides": "ಒಟ್ಟು ರೈಡ್‌ಗಳು",
        "total_earn": "ಒಟ್ಟು ಆದಾಯ",
        "online_hours": "ಆನ್‌ಲೈನ್ ಗಂಟೆಗಳು",
        "vs_yesterday": "ನಿನ್ನೆಗಿಂತ",
        "high_demand": "ಹೆಚ್ಚಿನ ಬೇಡಿಕೆ ನಿರೀಕ್ಷಿತ",
        "navigate_now": "ಈಗ ಹೋಗಿ",
        "logout_confirm": "ಯಶಸ್ವಿಯಾಗಿ ಲಾಗ್‌ಔಟ್!",
        "online": "ನೇರ",
        "thinking": "ಯೋಚಿಸುತ್ತಿದ್ದೇನೆ...",
        "clear_chat": "ತೆರವು",
        "powered_by": "Claude AI ಮೂಲಕ",
        "rides_today": "ಇಂದಿನ ರೈಡ್‌ಗಳು",
        "bonus_progress": "ಬೋನಸ್ ಪ್ರಗತಿ",
        "rides_to_bonus": "ರೈಡ್‌ ₹150 ಬೋನಸ್!",
        "streak": "ದಿನ ಸ್ಟ್ರೀಕ್ 🔥",
        "tip_of_day": "💡 ಸಲಹೆ",
        "navigate_zone": "ವಲಯಕ್ಕೆ ಹೋಗಿ",
        "current_hour": "ಈಗ",
        "earnings_bar": "ಆದಾಯ ಹೋಲಿಕೆ",
        "fuel_title": "ಇಂಧನ & ಖರ್ಚು",
        "add_fuel": "ಇಂಧನ ದಾಖಲಿಸಿ",
        "fuel_date": "ದಿನಾಂಕ",
        "fuel_liters": "ಲೀಟರ್",
        "fuel_cost": "ಖರ್ಚು (₹)",
        "fuel_odometer": "ಓಡೋಮೀಟರ್ (km)",
        "fuel_save": "ಉಳಿಸಿ",
        "fuel_history": "ಇಂಧನ ಇತಿಹಾಸ",
        "fuel_stats": "ಅಂಕಿಅಂಶಗಳು",
        "avg_mileage": "ಸರಾಸರಿ ಮೈಲೇಜ್",
        "total_fuel_cost": "ಒಟ್ಟು ಇಂಧನ ಖರ್ಚು",
        "fuel_per_km": "₹/ಕಿಮೀ",
        "expense_title": "ಇತರ ಖರ್ಚುಗಳು",
        "add_expense": "ಖರ್ಚು ಸೇರಿಸಿ",
        "expense_type": "ವಿಧ",
        "expense_amount": "ಮೊತ್ತ (₹)",
        "expense_note": "ಟಿಪ್ಪಣಿ",
        "expense_save": "ಸೇರಿಸಿ",
        "profit_loss": "ಲಾಭ / ನಷ್ಟ",
        "maint_title": "ವಾಹನ ನಿರ್ವಹಣೆ",
        "maint_schedule": "ನಿರ್ವಹಣೆ ವೇಳಾಪಟ್ಟಿ",
        "maint_log": "ಸೇವೆ ದಾಖಲೆ",
        "add_service": "ಸೇವೆ ಸೇರಿಸಿ",
        "service_type": "ಸೇವೆ ವಿಧ",
        "service_date": "ದಿನಾಂಕ",
        "service_cost": "ಖರ್ಚು (₹)",
        "service_notes": "ಟಿಪ್ಪಣಿ",
        "service_save": "ಉಳಿಸಿ",
        "next_service": "ಮುಂದಿನ ಸೇವೆ",
        "maint_reminders": "ಜ್ಞಾಪನೆಗಳು",
        "maint_history": "ಸೇವೆ ಇತಿಹಾಸ",
        "vehicle_health": "ವಾಹನ ಆರೋಗ್ಯ ಸ್ಕೋರ್",
        "overdue": "ತಡವಾದ",
        "due_soon": "ಶೀಘ್ರದಲ್ಲಿ",
        "good": "ಚೆನ್ನಾಗಿದೆ",
        "safety_title": "ಸುರಕ್ಷತೆ & SOS",
        "sos_title": "ತುರ್ತು SOS",
        "sos_desc": "ಅಪಾಯದಲ್ಲಿದ್ದೀರಾ? SOS ಒತ್ತಿ.",
        "sos_btn": "🚨 SOS ಕಳುಹಿಸಿ",
        "sos_sent": "🚨 SOS ಕಳುಹಿಸಲಾಗಿದೆ!",
        "safety_contacts": "ತುರ್ತು ಸಂಪರ್ಕಗಳು",
        "add_contact": "ಸಂಪರ್ಕ ಸೇರಿಸಿ",
        "contact_name": "ಹೆಸರು",
        "contact_phone": "ಫೋನ್",
        "contact_relation": "ಸಂಬಂಧ",
        "contact_save": "ಉಳಿಸಿ",
        "live_location": "ನೇರ ಸ್ಥಳ ಹಂಚಿಕೆ",
        "share_with": "ಹಂಚಿಕೊಳ್ಳಿ",
        "safety_checklist": "ದೈನಂದಿನ ಸುರಕ್ಷತೆ ಪರಿಶೀಲನೆ",
        "incident_report": "ಘಟನಾ ವರದಿ",
        "incident_type": "ಘಟನೆ ವಿಧ",
        "incident_desc": "ವಿವರಣೆ",
        "incident_zone": "Zone",
        "incident_time": "ಸಮಯ",
        "incident_submit": "ಸಲ್ಲಿಸಿ",
        "safety_score": "ಸುರಕ್ಷತೆ ಸ್ಕೋರ್",
        "safe_zones": "ಸುರಕ್ಷಿತ ಪ್ರದೇಶ",
        "night_mode": "ರಾತ್ರಿ ಸುರಕ್ಷತೆ ಮೋಡ್",
        "night_mode_desc": "ರಾತ್ರಿ 10 ಗಂಟೆ ನಂತರ 30 ನಿಮಿಷಕ್ಕೊಮ್ಮೆ ಸ್ಥಳ ಹಂಚಿ",
        "checkin_btn": "✅ ನಾನು ಸುರಕ್ಷಿತ",
        "last_checkin": "ಕೊನೆಯ check-in",
    },
}

# ── Constants ────────────────────────────────────────────────────────────────
ML_URL = "http://ml-service:8000"
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

ZONES_INFO = {
    "A": {"name": "Gandhipuram",   "name_ta": "காந்திபுரம்",   "name_hi": "गांधीपुरम",   "name_kn": "ಗಾಂಧೀಪುರಂ",
          "lat": 11.0168, "lon": 76.9558, "maps_q": "Gandhipuram+Coimbatore",
          "icon": "🏙️", "desc": "City centre, busy market", "safe": True},
    "B": {"name": "Ukkadam",       "name_ta": "உக்கடம்",       "name_hi": "उक्कडम",       "name_kn": "ಉಕ್ಕಡಂ",
          "lat": 10.9925, "lon": 76.9629, "maps_q": "Ukkadam+Coimbatore",
          "icon": "🚌", "desc": "Bus stand, steady rides", "safe": True},
    "C": {"name": "RS Puram",      "name_ta": "RS புரம்",       "name_hi": "आरएस पुरम",    "name_kn": "ಆರ್‌ಎಸ್ ಪುರಂ",
          "lat": 11.0050, "lon": 76.9479, "maps_q": "RS+Puram+Coimbatore",
          "icon": "💼", "desc": "IT offices, peak surge zone", "safe": True},
    "D": {"name": "Singanallur",   "name_ta": "சிங்கநல்லூர்",  "name_hi": "सिंगनल्लूर",   "name_kn": "ಸಿಂಗನಲ್ಲೂರು",
          "lat": 11.0018, "lon": 77.0232, "maps_q": "Singanallur+Coimbatore",
          "icon": "✈️", "desc": "Residential, airport nearby", "safe": True},
}

TIPS = {
    "English": [
        "Peak hours 7–10 AM & 5–9 PM = 30% more earnings. Be online!",
        "Complete 10 rides today for ₹150 bonus 💰",
        "RS Puram office crowd leaves at 6 PM — be there early!",
        "Accepting rides above 90% keeps your priority ranking high.",
        "Gandhipuram evenings (7–9 PM) have the highest ride density.",
    ],
    "தமிழ்": [
        "காலை 7–10, மாலை 5–9 — peak time, 30% அதிக வருமானம்!",
        "10 பயணங்கள் செய்தால் ₹150 போனஸ் 💰",
        "RS Puram office 6 PM-க்கு முடியும் — முன்னே போங்க!",
        "90% acceptance வச்சிருந்தா priority rank கிடைக்கும்.",
        "காந்திபுரம் இரவு 7–9 PM — அதிக rides கிடைக்கும்.",
    ],
    "हिंदी": [
        "सुबह 7–10 और शाम 5–9 पीक टाइम है — 30% ज्यादा कमाई!",
        "10 राइड पूरी करें और ₹150 बोनस पाएं 💰",
        "RS Puram ऑफिस शाम 6 बजे बंद होता है — पहले पहुंचें!",
        "90% से ज्यादा acceptance रखें — प्रायोरिटी रैंक मिलेगी।",
        "गांधीपुरम रात 7–9 PM — सबसे ज्यादा राइड मिलती हैं।",
    ],
    "ಕನ್ನಡ": [
        "ಬೆಳಿಗ್ಗೆ 7–10 ಮತ್ತು ಸಂಜೆ 5–9 ಪೀಕ್ ಟೈಮ್ — 30% ಹೆಚ್ಚು!",
        "10 ರೈಡ್ ಮಾಡಿ ₹150 ಬೋನಸ್ ಪಡೆಯಿರಿ 💰",
        "RS Puram ಆಫೀಸ್ ಸಂಜೆ 6 ಗಂಟೆಗೆ ಮುಗಿಯುತ್ತದೆ — ಮೊದಲೇ ಹೋಗಿ!",
        "90% acceptance ಇಟ್ಟುಕೊಳ್ಳಿ — priority rank ಸಿಗುತ್ತದೆ.",
        "ಗಾಂಧೀಪುರಂ ರಾತ್ರಿ 7–9 PM — ಹೆಚ್ಚು ರೈಡ್‌ ಸಿಗುತ್ತದೆ.",
    ],
}

MAINTENANCE_ITEMS = [
    {"name": "Engine Oil Change",   "icon": "🛢️", "interval_km": 5000,  "interval_days": 90,  "cost_est": 800},
    {"name": "Air Filter",          "icon": "🌬️", "interval_km": 10000, "interval_days": 180, "cost_est": 400},
    {"name": "Tyre Rotation",       "icon": "🔄", "interval_km": 8000,  "interval_days": 120, "cost_est": 300},
    {"name": "Brake Inspection",    "icon": "🛑", "interval_km": 15000, "interval_days": 180, "cost_est": 500},
    {"name": "Battery Check",       "icon": "🔋", "interval_km": 20000, "interval_days": 365, "cost_est": 200},
    {"name": "AC Servicing",        "icon": "❄️", "interval_km": 20000, "interval_days": 365, "cost_est": 1500},
    {"name": "Coolant Top-up",      "icon": "💧", "interval_km": 10000, "interval_days": 180, "cost_est": 200},
    {"name": "Wiper Blades",        "icon": "🌧️", "interval_km": 15000, "interval_days": 365, "cost_est": 300},
]

# ── Helper functions ─────────────────────────────────────────────────────────
def get_zone_name(zone, lang):
    z = ZONES_INFO[zone]
    if lang == "தமிழ்":   return z["name_ta"]
    if lang == "हिंदी":    return z["name_hi"]
    if lang == "ಕನ್ನಡ":   return z["name_kn"]
    return z["name"]

def google_maps_url(zone):
    z = ZONES_INFO[zone]
    return f"https://www.google.com/maps/dir/?api=1&destination={z['lat']},{z['lon']}&travelmode=driving"

def google_maps_search_url(zone):
    z = ZONES_INFO[zone]
    q = urllib.parse.quote(z["maps_q"])
    return f"https://www.google.com/maps/search/{q}/@{z['lat']},{z['lon']},15z"

def fetch_predictions(hour, dow):
    try:
        res = requests.get(f"{ML_URL}/predict?hour={hour}&dow={dow}", timeout=3)
        return res.json()
    except Exception:
        base = {"A": 1900, "B": 1300, "C": 2500, "D": 1500}
        peak = 1.4 if (7 <= hour <= 10 or 17 <= hour <= 21) else 1.0
        return sorted([
            {
                "zone": z,
                "predicted_demand": round(random.uniform(4, 12) * peak, 1),
                "predicted_earnings_per_hour": round(base[z] * peak + random.uniform(-150, 150), 1)
            }
            for z in ["A","B","C","D"]
        ], key=lambda x: -x["predicted_earnings_per_hour"])

def demand_bar_html(value, max_val=12, color="#6c5ce7"):
    pct = min(int((value / max_val) * 100), 100)
    blocks = pct // 10
    bar = "█" * blocks + "░" * (10 - blocks)
    return f'<span style="color:{color};font-family:monospace;font-size:16px;letter-spacing:2px;">{bar}</span> <span style="color:#fff;font-weight:700;">{value:.1f}</span>'

def earnings_bar_html(earn, max_earn=4000):
    pct = min(int((earn / max_earn) * 100), 100)
    return f'''
    <div style="background:#1e2240;border-radius:6px;height:10px;width:100%;margin-top:4px;">
        <div style="background:linear-gradient(90deg,#6c5ce7,#00c896);border-radius:6px;height:10px;width:{pct}%;transition:width 0.5s;"></div>
    </div>'''

def call_claude_api(messages, system_prompt):
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json", "anthropic-version": "2023-06-01"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 400, "system": system_prompt, "messages": messages},
            timeout=15
        )
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        return None
    except Exception:
        return None

def build_system_prompt(lang, driver_name, today_earn, best_zone, best_earn, demand_data, hour):
    zone_summary = "\n".join([
        f"  Zone {d['zone']} ({get_zone_name(d['zone'], 'English')}): {d['predicted_demand']:.1f} rides/hr, ₹{d['predicted_earnings_per_hour']:,.0f}/hr"
        for d in demand_data
    ])
    lang_instruction = {
        "English": "Respond in English.",
        "தமிழ்": "Respond in Tamil (தமிழ்) mixed with some English where needed (Tanglish is fine).",
        "हिंदी": "Respond in Hindi (हिंदी).",
        "ಕನ್ನಡ": "Respond in Kannada (ಕನ್ನಡ).",
    }.get(lang, "Respond in English.")

    # Fuel & maintenance context
    fuel_log    = st.session_state.get("fuel_log", [])
    expense_log = st.session_state.get("expense_log", [])
    svc_log     = st.session_state.get("service_log", [])
    total_fuel_spend  = sum(e["cost"] for e in fuel_log)
    total_other_spend = sum(e["amount"] for e in expense_log)

    return f"""You are an AI copilot assistant for a ride-hailing driver in Coimbatore, Tamil Nadu, India.
You help drivers maximize earnings, navigate to high-demand zones, track expenses, manage vehicle maintenance, and stay safe.

Driver context:
- Name: {driver_name}
- Today's earnings so far: ₹{today_earn:,}
- Current time: {hour}:00
- Best zone right now: Zone {best_zone} — ₹{best_earn:,.0f}/hr
- Total fuel spend (logged): ₹{total_fuel_spend:,}
- Other expenses (logged): ₹{total_other_spend:,}
- Services logged: {len(svc_log)}

Current demand across zones:
{zone_summary}

Zone locations in Coimbatore:
- Zone A: Gandhipuram (city center, busy market)
- Zone B: Ukkadam (bus stand, steady demand)
- Zone C: RS Puram (IT offices, peak surge zone)
- Zone D: Singanallur (residential, airport nearby)

Platform rules:
- Commission: 20% to platform, driver keeps 80%
- Bonus: ₹150 for 10+ rides/day, extra ₹50 for 5+ peak-hour rides
- Peak hours: 7–10 AM and 5–9 PM
- Fuel rate: ~₹6/km average consumption cost

You can answer questions about:
- Which zone to go to for best earnings
- Fuel efficiency tips and expense tracking advice
- Vehicle maintenance advice and when to service
- Safety tips during night driving or suspicious passengers
- Bonus targets and earnings optimization

Be concise, helpful, and encouraging. Use emojis sparingly. Answer in 2-4 sentences max.
{lang_instruction}"""

def score_color(score):
    if score >= 80: return "#00c896"
    if score >= 50: return "#ffa94d"
    return "#ff6b6b"

# ── Session state init ───────────────────────────────────────────────────────
defaults = {
    "logged_in": False,
    "driver_name": "",
    "vehicle_no": "",
    "lang": "English",
    "chat_history": [],
    "page": "Dashboard",
    "total_rides": random.randint(120, 140),
    "total_earnings_all": random.randint(4800, 5800),
    "rides_today": random.randint(5, 9),
    "streak_days": random.randint(3, 12),
    "tip_idx": random.randint(0, 4),
    # Fuel tracker
    "fuel_log": [
        {"date": (datetime.now() - timedelta(days=2)).strftime("%d %b"), "liters": 8.5, "cost": 918, "odometer": 45200},
        {"date": (datetime.now() - timedelta(days=5)).strftime("%d %b"), "liters": 7.2, "cost": 778, "odometer": 44820},
        {"date": (datetime.now() - timedelta(days=9)).strftime("%d %b"), "liters": 9.0, "cost": 972, "odometer": 44390},
    ],
    "expense_log": [
        {"date": (datetime.now() - timedelta(days=1)).strftime("%d %b"), "type": "Parking", "amount": 40, "note": "Gandhipuram mall"},
        {"date": (datetime.now() - timedelta(days=3)).strftime("%d %b"), "type": "Car Wash", "amount": 150, "note": "Weekly wash"},
        {"date": (datetime.now() - timedelta(days=6)).strftime("%d %b"), "type": "Toll", "amount": 60, "note": "Highway trip"},
    ],
    "current_odometer": 45580,
    # Maintenance
    "service_log": [
        {"date": (datetime.now() - timedelta(days=45)).strftime("%d %b %Y"), "type": "Engine Oil Change", "cost": 820, "odometer": 43000, "notes": "5W-30 oil used"},
        {"date": (datetime.now() - timedelta(days=90)).strftime("%d %b %Y"), "type": "Tyre Rotation",     "cost": 300, "odometer": 41000, "notes": "Front-back swap"},
        {"date": (datetime.now() - timedelta(days=120)).strftime("%d %b %Y"),"type": "Air Filter",        "cost": 420, "odometer": 39000, "notes": "Replaced filter"},
        {"date": (datetime.now() - timedelta(days=200)).strftime("%d %b %Y"),"type": "AC Servicing",      "cost": 1500,"odometer": 35000, "notes": "Gas refilled"},
    ],
    "last_service_odometer": {"Engine Oil Change": 43000, "Air Filter": 39000, "Tyre Rotation": 41000,
                               "Brake Inspection": 35000, "Battery Check": 30000, "AC Servicing": 35000,
                               "Coolant Top-up": 40000, "Wiper Blades": 38000},
    # Safety
    "emergency_contacts": [
        {"name": "Family Member", "phone": "9876500001", "relation": "Spouse"},
    ],
    "sos_active": False,
    "night_mode": False,
    "safety_checklist": {},
    "last_checkin": None,
    "incident_reports": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

T = LANG[st.session_state.lang]

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
body, .stApp { background-color: #0d0f1a !important; color: #ffffff; font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background-color: #12152b !important; border-right: 1px solid #1e2240; }
section[data-testid="stSidebar"] * { color: #cdd3f0 !important; }

.metric-box {
    background: linear-gradient(135deg, #1a1f3a 0%, #1e2445 100%);
    border-radius: 14px; padding: 18px 20px;
    border: 1px solid #2a2f50; position: relative; overflow: hidden; transition: transform 0.2s;
}
.metric-box:hover { transform: translateY(-2px); }
.metric-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #6c5ce7, #00c896);
}
.metric-box .label { font-size: 11px; color: #8892b0; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-box .value { font-size: 24px; font-weight: 800; color: #ffffff; }
.metric-box .delta-pos { font-size: 12px; color: #00c896; margin-top: 6px; font-weight: 500; }
.metric-box .delta-neg { font-size: 12px; color: #ff6b6b; margin-top: 6px; font-weight: 500; }
.metric-box .delta-neu { font-size: 12px; color: #ffa94d; margin-top: 6px; font-weight: 500; }

.section-card { background: #1a1f3a; border-radius: 14px; padding: 20px; border: 1px solid #2a2f50; margin-bottom: 16px; }
.section-title { font-size: 15px; font-weight: 700; color: #cdd3f0; margin-bottom: 14px; letter-spacing: 0.3px; }

.rec-card {
    background: linear-gradient(135deg, #1a1f3a 0%, #1e2445 100%);
    border-radius: 14px; padding: 20px; border: 1px solid #6c5ce7;
    margin-bottom: 16px; box-shadow: 0 0 20px rgba(108, 92, 231, 0.15);
}

.tip-card {
    background: linear-gradient(135deg, #1a2f1a, #0f1a0f);
    border: 1px solid #00c896; border-radius: 12px;
    padding: 14px 18px; margin-bottom: 16px;
    font-size: 14px; color: #cdd3f0; line-height: 1.5;
}
.bonus-card {
    background: linear-gradient(135deg, #2a1a3a, #1a1225);
    border: 1px solid #a29bfe; border-radius: 12px; padding: 16px;
    margin-bottom: 16px;
}
.streak-badge {
    background: linear-gradient(135deg, #ff6b35, #ff4500);
    color: white; border-radius: 20px; padding: 4px 14px;
    font-size: 13px; font-weight: 700; display: inline-block;
}
.earning-row {
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 0; border-bottom: 1px solid #1e2240;
}
.time-chip {
    background: #1e2240; color: #8892b0; border-radius: 6px;
    padding: 3px 8px; font-size: 11px; font-weight: 600;
}
.peak-chip {
    background: #3d1515; color: #ff6b6b; border-radius: 6px;
    padding: 3px 8px; font-size: 11px; font-weight: 700;
}
.zone-row { display:flex; align-items:center; justify-content:space-between; padding: 12px 0; border-bottom: 1px solid #1e2240; }
.zone-num { width:30px; height:30px; border-radius:50%; background: linear-gradient(135deg, #6c5ce7, #a29bfe); display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; color:#fff; margin-right:12px; flex-shrink:0; }
.ride-row { display:flex; align-items:center; justify-content:space-between; padding: 10px 0; border-bottom: 1px solid #1e2240; font-size:14px; }

.chat-container { height: 420px; overflow-y: auto; padding: 16px; background: #12152b; border-radius: 14px; border: 1px solid #2a2f50; margin-bottom: 12px; scroll-behavior: smooth; }
.chat-user { background: linear-gradient(135deg, #1e3a5f, #1a4070); border-radius: 18px 18px 4px 18px; padding: 10px 16px; margin: 8px 0 8px auto; max-width: 80%; color: #e0f0ff; font-size: 14px; width: fit-content; margin-left: auto; border: 1px solid #2a5080; }
.chat-bot { background: #1a1f3a; border-radius: 18px 18px 18px 4px; padding: 12px 16px; margin: 8px 0; max-width: 80%; color: #eee; font-size: 14px; border-left: 3px solid #6c5ce7; line-height: 1.5; }
.chat-meta { font-size: 10px; color: #8892b0; margin-top: 4px; }

.login-card { background: linear-gradient(135deg, #1a1f3a 0%, #12152b 100%); border-radius: 20px; padding: 40px; border: 1px solid #2a2f50; max-width: 420px; margin: 60px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; letter-spacing: 0.5px; }

/* Safety & SOS specific */
.sos-card {
    background: linear-gradient(135deg, #3d0000, #1a0000);
    border: 2px solid #ff3333; border-radius: 16px;
    padding: 24px; text-align: center; margin-bottom: 16px;
    box-shadow: 0 0 30px rgba(255, 50, 50, 0.25);
    position: relative; overflow: hidden;
}
.sos-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #ff3333, #ff6b6b, #ff3333);
    animation: pulse-bar 2s infinite;
}
@keyframes pulse-bar { 0%,100%{opacity:1} 50%{opacity:0.4} }
.sos-btn-label {
    font-size: 20px; font-weight: 900; color: #fff; letter-spacing: 1px;
}
.contact-card {
    background: #1a1f3a; border-radius: 12px; padding: 14px 16px;
    border: 1px solid #2a2f50; margin-bottom: 8px;
    display: flex; justify-content: space-between; align-items: center;
}
.safety-check-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid #1e2240; font-size: 14px;
}
.maint-card {
    border-radius: 12px; padding: 14px 16px; margin-bottom: 8px;
    border-left: 4px solid; display: flex; justify-content: space-between; align-items: center;
}
.health-ring {
    width: 120px; height: 120px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 900; margin: 0 auto 16px;
    position: relative;
}
.fuel-stat-box {
    background: #1a1f3a; border-radius: 12px; padding: 16px;
    border: 1px solid #2a2f50; text-align: center;
}
.log-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid #1e2240; font-size: 13px;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #12152b; }
::-webkit-scrollbar-thumb { background: #2a2f50; border-radius: 3px; }
.stButton > button { background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; transition: opacity 0.2s !important; }
.stButton > button:hover { opacity: 0.9 !important; }
div[data-testid="stMetric"] { background: #1a1f3a; border-radius: 12px; padding: 16px; border: 1px solid #2a2f50; }
a.map-link-btn {
    display: inline-block; background: linear-gradient(135deg, #1565c0, #0d47a1);
    color: white !important; text-decoration: none; padding: 8px 16px;
    border-radius: 8px; font-size: 13px; font-weight: 600;
    border: 1px solid #1976d2; transition: opacity 0.2s;
}
a.map-link-btn:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── LOGIN PAGE ───────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    lang_choice = st.selectbox("🌐 Language / மொழி / भाषा / ಭಾಷೆ", ["English","தமிழ்","हिंदी","ಕನ್ನಡ"], key="lang_login")
    st.session_state.lang = lang_choice
    T = LANG[lang_choice]

    st.markdown(f"""
    <div class="login-card">
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:52px; margin-bottom:8px;">🚗</div>
            <div style="font-size:26px; font-weight:800; color:#fff; letter-spacing:-0.5px;">{T['app_title']}</div>
            <div style="font-size:14px; color:#8892b0; margin-top:6px;">{T['tagline']}</div>
            <div style="margin-top:12px;"><span class="ai-badge">✦ AI-Powered</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.form("login_form"):
        name    = st.text_input(f"👤 {T['login_name']}", placeholder="Enter your name")
        phone   = st.text_input(f"📱 {T['login_phone']}", placeholder="Enter your phone number")
        vehicle = st.text_input(f"🚘 {T['login_vehicle']}", placeholder="Enter your vehicle number")
        submit  = st.form_submit_button(f"🚀 {T['login_btn']}", use_container_width=True)
        if submit:
            if name and phone and vehicle:
                st.session_state.logged_in   = True
                st.session_state.driver_name = name
                st.session_state.vehicle_no  = vehicle
                st.session_state.lang        = lang_choice
                st.rerun()
            else:
                st.error("Please fill all fields. / அனைத்து தகவல்களையும் நிரப்பவும்.")
    st.stop()

# ── POST LOGIN SETUP ─────────────────────────────────────────────────────────
T    = LANG[st.session_state.lang]
now  = datetime.now()
hour = now.hour
dow  = now.weekday()
data = fetch_predictions(hour, dow)
best = data[0] if isinstance(data, list) and data else {}
today_earn   = random.randint(2000, 3200)
rides_today  = st.session_state.rides_today
rides_needed = max(0, 10 - rides_today)
lang         = st.session_state.lang
tip_text     = TIPS.get(lang, TIPS["English"])[st.session_state.tip_idx % 5]

# Night mode auto-suggestion
if hour >= 22 or hour < 5:
    if not st.session_state.night_mode:
        st.warning("🌙 Night Safety Mode recommended — activate it in Safety & SOS page.")

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:12px 0 20px 0;">
        <div style="font-size:18px; font-weight:800; color:#fff; letter-spacing:-0.3px;">🚗 {T['app_title']}</div>
        <div style="font-size:11px; color:#8892b0; margin-top:2px;">{T['tagline']}</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigation", [
        T["nav_dashboard"], T["nav_heatmap"], T["nav_earnings"],
        T["nav_recommend"], T["nav_history"], T["nav_assistant"],
        T["nav_fuel"], T["nav_maintenance"], T["nav_safety"],
        T["nav_settings"],
    ], label_visibility="collapsed")

    st.divider()

    st.markdown(f"""
    <div style="padding:8px 0;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#6c5ce7,#a29bfe);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;color:#fff;flex-shrink:0;">
                {st.session_state.driver_name[0].upper()}
            </div>
            <div>
                <div style="font-weight:700;color:#fff;font-size:15px;">{st.session_state.driver_name}</div>
                <div style="color:#00c896;font-size:12px;font-weight:600;">⭐ 4.8 &nbsp; {T['active_driver']}</div>
            </div>
        </div>
        <div style="background:#12152b;border-radius:10px;padding:12px;font-size:13px;">
            <div style="color:#cdd3f0;margin:4px 0;">🚗 {st.session_state.vehicle_no}</div>
            <div style="color:#cdd3f0;margin:4px 0;">🛣 {T['total_rides']}: <b>{st.session_state.total_rides}</b></div>
            <div style="color:#cdd3f0;margin:4px 0;">💰 {T['total_earn']}: <b>₹{st.session_state.total_earnings_all:,}</b></div>
            <div style="color:#cdd3f0;margin:4px 0;">🕐 {T['online_hours']}: <b>32h 45m</b></div>
            <div style="margin-top:8px;"><span class="streak-badge">{T['streak']}: {st.session_state.streak_days}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.divider()
    lang_sel = st.selectbox("🌐 Language", ["English","தமிழ்","हिंदी","ಕನ್ನಡ"],
                             index=["English","தமிழ்","हिंदी","ಕನ್ನಡ"].index(st.session_state.lang))
    if lang_sel != st.session_state.lang:
        st.session_state.lang = lang_sel
        st.rerun()

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    if st.button(f"🚪 {T['nav_logout']}", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ── DASHBOARD ───────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
if page == T["nav_dashboard"]:
    col_title, col_live, col_time = st.columns([4, 1, 1])
    with col_title:
        st.markdown(f"### 📊 {T['nav_dashboard']}")
    with col_live:
        st.markdown(f"<div style='color:#00c896;font-weight:700;padding-top:10px;'>🟢 {T['online']}</div>", unsafe_allow_html=True)
    with col_time:
        st.markdown(f"<div style='color:#8892b0;padding-top:10px;text-align:right;font-size:13px;'>{now.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="tip-card">{T["tip_of_day"]}: {tip_text}</div>', unsafe_allow_html=True)

    bonus_pct   = min(int((rides_today / 10) * 100), 100)
    bonus_emoji = "🎉" if rides_today >= 10 else "🎯"
    bonus_msg   = "Bonus unlocked! ₹150 added!" if rides_today >= 10 else f"{rides_needed} {T['rides_to_bonus']}"
    bonus_color = "#00c896" if rides_today >= 10 else "#ffa94d"

    st.markdown(f"""
    <div class="bonus-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-weight:700;color:#cdd3f0;font-size:14px;">{bonus_emoji} {T['bonus_progress']}</div>
            <div style="font-weight:800;color:{bonus_color};font-size:16px;">{rides_today}/10 {T['rides_today']}</div>
        </div>
        <div style="background:#1e2240;border-radius:8px;height:14px;width:100%;">
            <div style="background:linear-gradient(90deg,#a29bfe,#6c5ce7);border-radius:8px;height:14px;width:{bonus_pct}%;transition:width 0.5s;"></div>
        </div>
        <div style="color:{bonus_color};font-size:12px;margin-top:6px;font-weight:600;">{bonus_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    exp_low  = int(best.get("predicted_earnings_per_hour", 400) * 0.8)
    exp_high = int(best.get("predicted_earnings_per_hour", 600) * 1.1)
    demand_score = random.randint(75, 95)
    idle_min     = random.randint(10, 30)
    acceptance   = random.randint(88, 97)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, label, value, delta, cls in [
        (c1, T['today_earn'],   f"₹{today_earn:,}",      f"▲ 18% {T['vs_yesterday']}", "delta-pos"),
        (c2, T['exp_earn'],     f"₹{exp_low}–{exp_high}", T['high_demand'],              "delta-neu"),
        (c3, T['demand_score'], f"{demand_score}/100",    T['very_high'],                "delta-pos"),
        (c4, T['idle_time'],    f"{idle_min} min",        f"▼ 15% {T['vs_yesterday']}",  "delta-pos"),
        (c5, T['acceptance'],   f"{acceptance}%",         f"▲ 5% {T['vs_yesterday']}",   "delta-pos"),
    ]:
        with col:
            st.markdown(f"""<div class="metric-box">
                <div class="label">{label}</div><div class="value">{value}</div>
                <div class="{cls}">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown(f'<div class="section-card"><div class="section-title">🗺 {T["live_heatmap"]}</div>', unsafe_allow_html=True)
        cols_h = st.columns(4)
        for i, item in enumerate(data):
            z     = item["zone"]
            zname = get_zone_name(z, lang)
            d     = item["predicted_demand"]
            earn  = item["predicted_earnings_per_hour"]
            zi    = ZONES_INFO[z]

            if d >= 10:   bg,clr,dot,lvl_t = "#3d1515","#ff6b6b","🔴", T["very_high"]
            elif d >= 7:  bg,clr,dot,lvl_t = "#3d2a15","#ffa94d","🟠", T["high"]
            elif d >= 5:  bg,clr,dot,lvl_t = "#1a3d15","#69db7c","🟡", T["medium"]
            else:         bg,clr,dot,lvl_t = "#15283d","#74c0fc","🟢", T["low"]

            bar_html = earnings_bar_html(earn)
            maps_url = google_maps_url(z)
            safe_icon = "✅" if zi["safe"] else "⚠️"

            with cols_h[i]:
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {clr};border-radius:12px;
                            padding:14px 10px;text-align:center;margin-bottom:8px;">
                    <div style="font-size:24px;">{zi['icon']}</div>
                    <div style="font-weight:700;color:#fff;font-size:14px;margin-top:4px;">Zone {z}</div>
                    <div style="color:{clr};font-size:11px;font-weight:700;">{zname}</div>
                    <div style="color:#aaa;font-size:10px;margin-top:2px;">{zi['desc']}</div>
                    <div style="font-size:10px;color:#8892b0;margin-top:2px;">{safe_icon} Safe zone</div>
                    <div style="margin-top:8px;">
                        <div style="color:#8892b0;font-size:11px;">🚗 {d:.1f} rides/hr</div>
                        <div style="color:#00c896;font-size:17px;font-weight:800;margin:4px 0;">₹{earn:,.0f}/hr</div>
                        {bar_html}
                        <div style="font-size:10px;color:{clr};font-weight:700;margin-top:6px;">{dot} {lvl_t}</div>
                    </div>
                    <a href="{maps_url}" target="_blank" style="display:block;margin-top:10px;
                       background:rgba(255,255,255,0.1);color:#fff;border-radius:8px;
                       padding:6px;font-size:11px;font-weight:600;text-decoration:none;
                       border:1px solid rgba(255,255,255,0.2);">
                        📍 Google Maps
                    </a>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;gap:16px;padding:8px 0;font-size:12px;color:#8892b0;">
            <span>🟢 {T['low']}</span><span>🟡 {T['medium']}</span>
            <span>🟠 {T['high']}</span><span>🔴 {T['very_high']}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="section-card"><div class="section-title">📋 {T["top_zones"]}</div>', unsafe_allow_html=True)
        for i, item in enumerate(data):
            z     = item["zone"]
            zname = get_zone_name(z, lang)
            d     = item["predicted_demand"]
            earn  = item["predicted_earnings_per_hour"]
            lvl   = "very_high" if d >= 10 else "high" if d >= 7 else "medium" if d >= 5 else "low"
            clr   = {"very_high":"#ff6b6b","high":"#ffa94d","medium":"#69db7c","low":"#74c0fc"}[lvl]
            gain  = ["+25%","+18%","+10%","+8%"][i]
            bar   = demand_bar_html(d, color=clr)
            zi    = ZONES_INFO[z]
            maps_url = google_maps_url(z)
            st.markdown(f"""
            <div class="zone-row">
                <div style="display:flex;align-items:center;gap:12px;flex:1;">
                    <div class="zone-num">{i+1}</div>
                    <div style="flex:1;">
                        <div style="font-weight:700;color:#fff;font-size:14px;">{zi['icon']} Zone {z} – {zname}</div>
                        <div style="margin-top:4px;">{bar}</div>
                        <div style="color:#8892b0;font-size:11px;margin-top:2px;">{zi['desc']}</div>
                    </div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:12px;">
                    <div style="color:#00c896;font-weight:800;font-size:15px;">₹{earn:,.0f}/hr</div>
                    <div style="color:#69db7c;font-size:12px;font-weight:600;">{gain}</div>
                    <a href="{maps_url}" target="_blank" style="display:inline-block;margin-top:4px;
                       background:#1e2a5f;color:#74c0fc;border-radius:6px;padding:3px 8px;
                       font-size:11px;text-decoration:none;border:1px solid #2a3f80;">📍 Navigate</a>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        best_zone = best.get("zone","C")
        bname     = get_zone_name(best_zone, lang)
        exp_earn  = best.get("predicted_earnings_per_hour", 500)
        maps_url  = google_maps_url(best_zone)

        st.markdown(f"""
        <div class="rec-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                <div style="font-weight:700;color:#cdd3f0;font-size:15px;">🎯 {T['ai_rec']}</div>
                <div style="background:#6c5ce7;color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;">{T['best_option']}</div>
            </div>
            <div style="font-size:17px;font-weight:800;color:#fff;margin-bottom:16px;">
                {ZONES_INFO[best_zone]['icon']} {T['move_to']} Zone {best_zone} – {bname}
                <span style="color:#00c896;font-size:13px;font-weight:600;"> +25%</span>
            </div>
            <div style="display:flex;flex-direction:column;gap:0;font-size:14px;">
                <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #2a2f50;">
                    <span style="color:#8892b0;">{T['exp_earnings']}</span>
                    <span style="color:#fff;font-weight:700;">₹{int(exp_earn*0.8):,}–₹{int(exp_earn*1.1):,}/hr</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #2a2f50;">
                    <span style="color:#8892b0;">{T['distance']}</span>
                    <span style="color:#fff;font-weight:700;">2.3 km · ~6 min</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #2a2f50;">
                    <span style="color:#8892b0;">{T['demand']}</span>
                    <span style="color:#ff6b6b;font-weight:700;">{T['very_high']}</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:10px 0;">
                    <span style="color:#8892b0;">{T['idle_reduction']}</span>
                    <span style="color:#00c896;font-weight:700;">-26%</span>
                </div>
            </div>
            <a href="{maps_url}" target="_blank" style="display:block;margin-top:14px;
               background:linear-gradient(135deg,#1565c0,#0d47a1);color:#fff;
               border-radius:10px;padding:10px 16px;font-size:14px;font-weight:700;
               text-decoration:none;text-align:center;border:1px solid #1976d2;">
               🗺 {T['get_directions']}
            </a>
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<div class="section-card"><div class="section-title">📈 {T["earn_predict"]}</div>', unsafe_allow_html=True)
        future_hours = [(hour + i) % 24 for i in range(4)]
        max_e = 0
        rows  = []
        for fh in future_hours:
            d  = fetch_predictions(fh, dow)
            e  = d[0]["predicted_earnings_per_hour"] if isinstance(d, list) and d else 400
            bz = d[0]["zone"] if isinstance(d, list) and d else "?"
            is_peak = (7 <= fh <= 10 or 17 <= fh <= 21)
            rows.append({"fh": fh, "earn": e, "zone": bz, "peak": is_peak})
            max_e = max(max_e, e)

        for r in rows:
            pct  = int((r["earn"] / max(max_e, 1)) * 100)
            clr  = "#ff6b6b" if r["peak"] else "#6c5ce7"
            chip = f'<span class="peak-chip">🔥 Peak</span>' if r["peak"] else f'<span class="time-chip">{T["current_hour"] if r["fh"]==hour else ""}</span>'
            st.markdown(f"""
            <div class="earning-row">
                <div style="min-width:55px;color:#8892b0;font-size:13px;">{r['fh']}:00 {chip}</div>
                <div style="flex:1;margin:0 12px;">
                    <div style="background:#1e2240;border-radius:4px;height:8px;">
                        <div style="background:{clr};border-radius:4px;height:8px;width:{pct}%;"></div>
                    </div>
                </div>
                <div style="min-width:90px;text-align:right;">
                    <span style="color:#00c896;font-weight:700;font-size:13px;">₹{int(r['earn']):,}/hr</span>
                    <span style="color:#8892b0;font-size:11px;margin-left:4px;">Z{r['zone']}</span>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="section-card"><div class="section-title">🚖 {T["recent_rides"]}</div>', unsafe_allow_html=True)
        recent = [
            {"from": "Zone C", "to": "Zone A", "time": "7:15 PM", "earn": 186, "km": 6.2},
            {"from": "Zone A", "to": "Zone D", "time": "6:45 PM", "earn": 245, "km": 9.1},
            {"from": "Zone B", "to": "Zone C", "time": "6:20 PM", "earn": 158, "km": 3.8},
            {"from": "Zone D", "to": "Zone A", "time": "5:50 PM", "earn": 210, "km": 7.5},
        ]
        for r in recent:
            stars = "⭐" * random.randint(4,5)
            st.markdown(f"""
            <div class="ride-row">
                <div>
                    <div style="color:#cdd3f0;font-weight:500;font-size:13px;">{r['from']} → {r['to']}</div>
                    <div style="color:#8892b0;font-size:11px;">{r['time']} · {r['km']} km · {stars}</div>
                </div>
                <div style="color:#00c896;font-weight:800;font-size:15px;">₹{r['earn']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ── HEATMAP PAGE ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_heatmap"]:
    st.markdown(f"### 🗺 {T['nav_heatmap']}")
    hour_sel = st.slider("🕐 Hour", 0, 23, hour)
    dow_sel  = st.selectbox("📅 Day", range(7), format_func=lambda x: DAYS[x], index=dow)
    snap     = fetch_predictions(hour_sel, dow_sel)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, item in enumerate(sorted(snap, key=lambda x: x["zone"])):
        z     = item["zone"]
        zname = get_zone_name(z, lang)
        d     = item["predicted_demand"]
        earn  = item["predicted_earnings_per_hour"]
        zi    = ZONES_INFO[z]
        maps_url = google_maps_url(z)

        if d >= 10:   bg,clr,dot = "#3d1515","#ff6b6b","🔴"
        elif d >= 7:  bg,clr,dot = "#3d2a15","#ffa94d","🟠"
        elif d >= 5:  bg,clr,dot = "#1a3d15","#69db7c","🟡"
        else:         bg,clr,dot = "#15283d","#74c0fc","🟢"

        bar_html = earnings_bar_html(earn)
        with cols[i]:
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {clr};border-radius:14px;padding:18px;text-align:center;margin-bottom:12px;">
                <div style="font-size:32px;">{zi['icon']}</div>
                <div style="font-size:18px;font-weight:800;color:#fff;margin-top:6px;">Zone {z}</div>
                <div style="color:{clr};font-size:13px;font-weight:700;">{zname}</div>
                <div style="color:#aaa;font-size:11px;">{zi['desc']}</div>
                <div style="color:#cdd3f0;font-size:14px;margin-top:8px;">{d:.1f} rides/hr</div>
                <div style="color:#00c896;font-size:22px;font-weight:800;margin-top:4px;">₹{earn:,.0f}/hr</div>
                {bar_html}
                <a href="{maps_url}" target="_blank"
                   style="display:block;margin-top:12px;background:rgba(255,255,255,0.1);
                   color:#fff;border-radius:8px;padding:8px;font-size:12px;font-weight:700;
                   text-decoration:none;border:1px solid rgba(255,255,255,0.25);">
                   📍 {T['navigate_now']} → Google Maps
                </a>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"### 📊 24-Hour Demand Heatmap — {DAYS[dow_sel]}")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:60px 1fr 1fr 1fr 1fr;gap:4px;margin-bottom:8px;">
        <div style="color:#8892b0;font-size:11px;">Hour</div>
        <div style="color:#a29bfe;font-size:11px;font-weight:700;text-align:center;">🏙️ Zone A</div>
        <div style="color:#a29bfe;font-size:11px;font-weight:700;text-align:center;">🚌 Zone B</div>
        <div style="color:#a29bfe;font-size:11px;font-weight:700;text-align:center;">💼 Zone C</div>
        <div style="color:#a29bfe;font-size:11px;font-weight:700;text-align:center;">✈️ Zone D</div>
    </div>""", unsafe_allow_html=True)

    for h in range(6, 23):
        d = fetch_predictions(h, dow_sel)
        row_vals = {item["zone"]: item["predicted_demand"] for item in d}
        is_peak  = 7 <= h <= 10 or 17 <= h <= 21
        hour_bg  = "background:#2a1530;border-left:3px solid #ff6b6b;" if is_peak else ""
        peak_tag = "🔥" if is_peak else ""
        cells = ""
        for z in ["A","B","C","D"]:
            v = row_vals.get(z, 0)
            pct = int((v / 12) * 100)
            if v >= 10:   clr = "#ff6b6b"
            elif v >= 7:  clr = "#ffa94d"
            elif v >= 5:  clr = "#69db7c"
            else:         clr = "#74c0fc"
            cells += f"""<div style="text-align:center;">
                <div style="background:#1e2240;border-radius:4px;height:6px;width:80%;margin:0 auto 2px;">
                    <div style="background:{clr};border-radius:4px;height:6px;width:{pct}%;"></div>
                </div>
                <span style="color:{clr};font-size:12px;font-weight:700;">{v:.0f}</span>
            </div>"""
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:60px 1fr 1fr 1fr 1fr;gap:4px;
                    padding:5px 4px;border-radius:6px;{hour_bg}margin-bottom:2px;align-items:center;">
            <div style="color:#8892b0;font-size:12px;">{h}:00 {peak_tag}</div>
            {cells}
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ── EARNINGS PAGE ────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_earnings"]:
    st.markdown(f"### 💰 {T['nav_earnings']}")
    week_earn  = random.randint(12000, 18000)
    month_earn = random.randint(42000, 58000)

    c1, c2, c3 = st.columns(3)
    c1.metric(T["today_earn"],  f"₹{today_earn:,}", "▲ 18%")
    c2.metric("This Week",      f"₹{week_earn:,}",  "▲ 12%")
    c3.metric("This Month",     f"₹{month_earn:,}", "▲ 8%")

    st.markdown(f"### 📊 {T['earn_predict']}")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    hourly_data = []
    for h in range(6, 24):
        d = fetch_predictions(h, dow)
        e = d[0]["predicted_earnings_per_hour"] if isinstance(d, list) and d else 0
        z = d[0]["zone"] if isinstance(d, list) and d else "?"
        hourly_data.append({"h": h, "earn": round(e), "zone": z})

    max_e = max(r["earn"] for r in hourly_data) if hourly_data else 3000
    for r in hourly_data:
        is_peak = 7 <= r["h"] <= 10 or 17 <= r["h"] <= 21
        pct     = int((r["earn"] / max_e) * 100)
        clr     = "#ff6b6b" if is_peak else "#6c5ce7"
        bg_row  = "background:#1a0f20;" if is_peak else ""
        tag     = "🔥" if is_peak else "  "
        cur_tag = "← Now" if r["h"] == hour else ""
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:5px 6px;border-radius:6px;{bg_row}margin-bottom:2px;">
            <div style="min-width:55px;color:#8892b0;font-size:12px;">{tag}{r['h']}:00</div>
            <div style="flex:1;">
                <div style="background:#1e2240;border-radius:4px;height:10px;">
                    <div style="background:{clr};border-radius:4px;height:10px;width:{pct}%;"></div>
                </div>
            </div>
            <div style="min-width:110px;text-align:right;font-size:12px;">
                <span style="color:#00c896;font-weight:700;">₹{r['earn']:,}/hr</span>
                <span style="color:#8892b0;"> Z{r['zone']}</span>
                <span style="color:#ffa94d;font-size:10px;"> {cur_tag}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🧮 Fare Breakdown Calculator")
    col1, col2 = st.columns(2)
    with col1:
        base     = st.number_input("Base fare (₹)", 50, 1000, 220, 10)
        dist_km  = st.number_input("Distance (km)", 1.0, 50.0, 8.5, 0.5)
        is_peak  = st.checkbox("Peak hour surge", value=(7 <= hour <= 10 or 17 <= hour <= 21))
    with col2:
        bonus    = st.number_input("Bonus (₹)", 0, 500, 50)
        comm_pct = st.slider("Commission %", 10, 30, 20)

    dist_chg   = round(dist_km * 12, 2)
    surge      = round((base + dist_chg) * 0.3, 2) if is_peak else 0
    gross      = base + dist_chg + surge
    commission = round(gross * comm_pct / 100, 2)
    fuel_c     = round(dist_km * 6, 2)
    net        = round(gross - commission + bonus - fuel_c, 2)
    margin     = (net / gross * 100) if gross else 0

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    items = [
        ("Base Fare",        f"₹{base}",           "#cdd3f0",  1),
        (f"Distance {dist_km}km@₹12", f"+₹{dist_chg}", "#69db7c", 1),
        ("Peak Surge 30%",   f"+₹{surge}",          "#ffa94d",  1 if is_peak else 0),
        ("Gross Total",      f"₹{gross:.0f}",       "#fff",     1),
        (f"Commission {comm_pct}%", f"-₹{commission:.0f}", "#ff6b6b", 1),
        ("Bonus",            f"+₹{bonus}",           "#69db7c",  1),
        ("Fuel Cost",        f"-₹{fuel_c}",          "#ff6b6b",  1),
        ("💵 NET TAKE-HOME", f"₹{net:.0f}",          "#00c896",  1),
    ]
    for label, amt, clr, show in items:
        if not show: continue
        bold = "font-weight:800;font-size:16px;" if "NET" in label else ""
        sep  = "border-top:1px solid #6c5ce7;margin-top:6px;padding-top:6px;" if "NET" in label else ""
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:6px 0;{sep}">
            <span style="color:#8892b0;font-size:13px;">{label}</span>
            <span style="color:{clr};{bold}">{amt}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("💵 Your Take-Home", f"₹{net:.0f}", f"{margin:.1f}% margin")
    c2.metric("📊 Gross Fare",     f"₹{gross:.0f}", f"Surge: {'Yes ✅' if is_peak else 'No'}")

# ════════════════════════════════════════════════════════════════════════════
# ── RECOMMENDATIONS ──────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_recommend"]:
    st.markdown(f"### 🎯 {T['nav_recommend']}")
    hour_sel = st.slider("⏰ Simulate for hour", 0, 23, hour)

    st.subheader("🗓 Full Day Earnings Plan")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:120px 1fr 80px 90px 80px;gap:4px;margin-bottom:8px;">
        <div style="color:#8892b0;font-size:11px;font-weight:700;">HOUR</div>
        <div style="color:#8892b0;font-size:11px;font-weight:700;">BEST ZONE</div>
        <div style="color:#8892b0;font-size:11px;font-weight:700;">RIDES/HR</div>
        <div style="color:#8892b0;font-size:11px;font-weight:700;">₹/HR</div>
        <div style="color:#8892b0;font-size:11px;font-weight:700;">MAP</div>
    </div>""", unsafe_allow_html=True)

    for h in range(6, 23):
        d = fetch_predictions(h, dow)
        if not (isinstance(d, list) and d): continue
        b        = d[0]
        z        = b["zone"]
        zname    = get_zone_name(z, lang)
        zi       = ZONES_INFO[z]
        is_ph    = 7 <= h <= 10 or 17 <= h <= 21
        bg_row   = "background:#2a1530;border-radius:6px;" if is_ph else ""
        peak_tag = "🔥" if is_ph else "  "
        maps_url = google_maps_url(z)
        earn_clr = "#ff6b6b" if is_ph else "#00c896"
        cur_tag  = "← Now" if h == hour else ""

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:120px 1fr 80px 90px 80px;gap:4px;
                    padding:7px 6px;{bg_row}margin-bottom:2px;align-items:center;">
            <div style="color:#8892b0;font-size:12px;">{peak_tag} {h}:00–{h+1}:00 <span style="color:#ffa94d;font-size:10px;">{cur_tag}</span></div>
            <div style="color:#fff;font-size:13px;font-weight:600;">{zi['icon']} Zone {z} – {zname}</div>
            <div style="color:#cdd3f0;font-size:13px;">{b['predicted_demand']:.1f}</div>
            <div style="color:{earn_clr};font-weight:700;font-size:13px;">₹{b['predicted_earnings_per_hour']:,.0f}</div>
            <div><a href="{maps_url}" target="_blank" style="color:#74c0fc;font-size:11px;text-decoration:none;background:#1e2240;padding:3px 6px;border-radius:4px;">📍 Go</a></div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🔀 Zone Switch Calculator")
    c1, c2 = st.columns(2)
    cur = c1.selectbox("Current Zone", list(ZONES_INFO.keys()))
    tgt = c2.selectbox("Target Zone",  list(ZONES_INFO.keys()), index=2)

    distances = {("A","B"):4.2,("A","C"):6.1,("A","D"):9.3,("B","C"):3.8,("B","D"):7.1,("C","D"):5.5}
    dist      = distances.get(tuple(sorted([cur, tgt])), round(random.uniform(3, 10), 1))
    fuel_move = round(dist * 6, 1)
    snap      = fetch_predictions(hour_sel, dow)
    cur_earn  = next((x["predicted_earnings_per_hour"] for x in snap if x["zone"]==cur), 0)
    tgt_earn  = next((x["predicted_earnings_per_hour"] for x in snap if x["zone"]==tgt), 0)
    gain      = tgt_earn - cur_earn

    m1, m2, m3 = st.columns(3)
    m1.metric("Distance to Move", f"{dist:.1f} km")
    m2.metric("Fuel Cost",        f"₹{fuel_move}")
    m3.metric("Earnings Gain/hr", f"₹{gain:+.0f}")

    if cur == tgt:
        st.info("You're already in this zone!")
    elif gain > fuel_move * 2:
        st.success(f"✅ Worth it! Moving to Zone {tgt} nets ₹{gain - fuel_move:.0f} more after fuel.")
        maps_url = google_maps_url(tgt)
        st.markdown(f'<a href="{maps_url}" target="_blank" class="map-link-btn">🗺 Navigate to Zone {tgt} ({get_zone_name(tgt, lang)}) →</a>', unsafe_allow_html=True)
    elif gain > 0:
        st.info(f"⚠️ Marginal gain of ₹{gain:.0f}/hr after ₹{fuel_move} fuel. Your call.")
    else:
        st.warning(f"❌ Stay in Zone {cur} — switching loses ₹{abs(gain):.0f}/hr.")

# ════════════════════════════════════════════════════════════════════════════
# ── RIDE HISTORY ──────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_history"]:
    st.markdown(f"### 🚖 {T['nav_history']}")
    fc1, fc2 = st.columns(2)
    filter_date = fc1.selectbox("📅 Period", ["Today","Last 7 days","Last 30 days","All time"])
    filter_zone = fc2.selectbox("📍 Zone", ["All Zones"] + [f"Zone {z}" for z in ZONES_INFO.keys()])

    rides = []
    t = now
    for i in range(30):
        t -= timedelta(minutes=random.randint(20, 60))
        zones = list(ZONES_INFO.keys())
        fz, tz = random.sample(zones, 2)
        earn   = random.randint(120, 350)
        dist   = round(random.uniform(3, 12), 1)
        rides.append({
            "Date":      t.strftime("%d %b"),
            "Time":      t.strftime("%I:%M %p"),
            "From":      f"Zone {fz} ({get_zone_name(fz, lang)})",
            "To":        f"Zone {tz} ({get_zone_name(tz, lang)})",
            "Dist (km)": dist,
            "Earnings":  f"₹{earn}",
            "Rating":    "⭐" * random.randint(4, 5),
        })

    rides_df = pd.DataFrame(rides)
    if filter_zone != "All Zones":
        rides_df = rides_df[rides_df["From"].str.startswith(filter_zone)]

    st.dataframe(rides_df, use_container_width=True, hide_index=True)

    total = sum(int(r["Earnings"][1:]) for r in rides)
    r1, r2, r3 = st.columns(3)
    r1.metric("Total Rides Shown", len(rides_df))
    r2.metric("Total Earned",      f"₹{total:,}")
    r3.metric("Avg per Ride",      f"₹{total//max(len(rides_df),1)}")

# ════════════════════════════════════════════════════════════════════════════
# ── AI ASSISTANT ──────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_assistant"]:
    st.markdown(f"### 🤖 {T['ai_assistant']}")

    col_hdr, col_badge = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div style='color:#8892b0;font-size:13px;margin-bottom:12px;'>Ask anything about earnings, zones, fuel costs, maintenance, safety, or tips to drive smarter.</div>", unsafe_allow_html=True)
    with col_badge:
        st.markdown(f"<div class='ai-badge' style='margin-top:4px;'>✦ {T['powered_by']}</div>", unsafe_allow_html=True)

    best_zone_key = best.get("zone", "C")
    best_earn_val = best.get("predicted_earnings_per_hour", 2500)

    system_prompt = build_system_prompt(
        lang, st.session_state.driver_name, today_earn,
        best_zone_key, best_earn_val, data, hour
    )

    st.markdown('<div class="chat-container" id="chatbox">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        greet = {
            "English": f"Hi {st.session_state.driver_name}! 👋 I'm your AI Copilot. Zone {best_zone_key} has the best earnings at ₹{best_earn_val:,.0f}/hr. I can also help with fuel tracking, maintenance reminders, and safety tips!",
            "தமிழ்":   f"வணக்கம் {st.session_state.driver_name}! 👋 Zone {best_zone_key} சிறந்தது — ₹{best_earn_val:,.0f}/மணி. எரிபொருள், பராமரிப்பு, பாதுகாப்பு — எதையும் கேளுங்கள்!",
            "हिंदी":   f"नमस्ते {st.session_state.driver_name}! 👋 Zone {best_zone_key} सबसे अच्छा — ₹{best_earn_val:,.0f}/घंटा। ईंधन, रखरखाव, सुरक्षा — कुछ भी पूछें!",
            "ಕನ್ನಡ":   f"ನಮಸ್ಕಾರ {st.session_state.driver_name}! 👋 Zone {best_zone_key} ಉತ್ತಮ — ₹{best_earn_val:,.0f}/ಗಂಟೆ. ಇಂಧನ, ನಿರ್ವಹಣೆ, ಸುರಕ್ಷತೆ — ಏನಾದರೂ ಕೇಳಿ!",
        }
        st.markdown(f'<div class="chat-bot">{greet.get(lang, greet["English"])}<div class="chat-meta">Just now · AI Copilot</div></div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">{msg["content"]}<div class="chat-meta">AI Copilot</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    quick_labels = {
        "English": ["💳 Payment help","📍 Best zone now","⛽ Fuel save tips","💰 Commission %","🎁 Earn bonus","🔧 Oil change due?","🌙 Night safety","⭐ Improve rating"],
        "தமிழ்":   ["💳 பணம் பிரச்னை","📍 சிறந்த zone","⛽ பெட்ரோல் சேமிப்பு","💰 கமிஷன்","🎁 போனஸ்","🔧 Oil மாற்றல்","🌙 இரவு பாதுகாப்பு","⭐ ரேட்டிங்"],
        "हिंदी":   ["💳 पेमेंट","📍 बेस्ट जोन","⛽ ईंधन बचत","💰 कमीशन","🎁 बोनस","🔧 ऑयल चेंज","🌙 रात सुरक्षा","⭐ रेटिंग"],
        "ಕನ್ನಡ":   ["💳 ಪಾವತಿ","📍 ಉತ್ತಮ ವಲಯ","⛽ ಇಂಧನ ಉಳಿತಾಯ","💰 ಕಮಿಷನ್","🎁 ಬೋನಸ್","🔧 ಆಯಿಲ್ ಬದಲಾಯಿಸಿ","🌙 ರಾತ್ರಿ ಸುರಕ್ಷತೆ","⭐ ರೇಟಿಂಗ್"],
    }
    ql = quick_labels.get(lang, quick_labels["English"])
    cols_q = st.columns(4)
    for i, label in enumerate(ql):
        if cols_q[i % 4].button(label, use_container_width=True, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": label})
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
            with st.spinner(T.get("thinking", "Thinking...")):
                reply = call_claude_api(api_messages, system_prompt)
            if not reply:
                fallbacks = {"English": "Connection issue. Please try again.", "தமிழ்": "மீண்டும் முயற்சிக்கவும்.", "हिंदी": "फिर कोशिश करें।", "ಕನ್ನಡ": "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."}
                reply = fallbacks.get(lang, fallbacks["English"])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    if prompt := st.chat_input(T["ask_placeholder"]):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
        with st.spinner(T.get("thinking", "Thinking...")):
            reply = call_claude_api(api_messages, system_prompt)
        if not reply:
            fallbacks = {"English": "Sorry, couldn't connect. Try again.", "தமிழ்": "மன்னிக்கவும், மீண்டும் முயற்சிக்கவும்.", "हिंदी": "माफ करें, फिर कोशिश करें।", "ಕನ್ನಡ": "ಕ್ಷಮಿಸಿ, ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."}
            reply = fallbacks.get(lang, fallbacks["English"])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    col_clr1, col_clr2 = st.columns([4, 1])
    with col_clr2:
        if st.button(f"🗑️ {T.get('clear_chat','Clear')}", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ── FUEL & EXPENSE TRACKER ───────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_fuel"]:
    st.markdown(f"### ⛽ {T['fuel_title']}")

    tab_fuel, tab_expense, tab_summary = st.tabs(["⛽ Fuel Log", "💸 Other Expenses", "📊 P&L Summary"])

    with tab_fuel:
        col_form, col_stats = st.columns([1, 1])

        with col_form:
            st.markdown(f'<div class="section-card"><div class="section-title">➕ {T["add_fuel"]}</div>', unsafe_allow_html=True)
            with st.form("fuel_form"):
                f_date = st.date_input(T["fuel_date"], value=now.date())
                f_col1, f_col2 = st.columns(2)
                f_liters = f_col1.number_input(T["fuel_liters"], 1.0, 60.0, 8.0, 0.5)
                f_cost   = f_col2.number_input(T["fuel_cost"],   50, 7000, 864, 10)
                f_odo    = st.number_input(T["fuel_odometer"], 0, 999999, st.session_state.current_odometer, 10)
                submitted = st.form_submit_button(f"💾 {T['fuel_save']}", use_container_width=True)
                if submitted:
                    st.session_state.fuel_log.insert(0, {
                        "date": f_date.strftime("%d %b"),
                        "liters": f_liters,
                        "cost": f_cost,
                        "odometer": f_odo,
                    })
                    st.session_state.current_odometer = f_odo
                    st.success("✅ Fuel entry saved!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col_stats:
            fuel_log = st.session_state.fuel_log
            if len(fuel_log) >= 2:
                total_liters = sum(e["liters"] for e in fuel_log)
                total_cost   = sum(e["cost"]   for e in fuel_log)
                km_range     = fuel_log[0]["odometer"] - fuel_log[-1]["odometer"]
                mileage      = round(km_range / total_liters, 1) if total_liters > 0 else 0
                cost_per_km  = round(total_cost / km_range, 2) if km_range > 0 else 0
            else:
                total_liters = sum(e["liters"] for e in fuel_log) if fuel_log else 0
                total_cost   = sum(e["cost"]   for e in fuel_log) if fuel_log else 0
                mileage      = 14.2
                cost_per_km  = 7.6

            st.markdown(f'<div class="section-card"><div class="section-title">📊 {T["fuel_stats"]}</div>', unsafe_allow_html=True)

            sc1, sc2, sc3 = st.columns(3)
            for col, icon, label, val in [
                (sc1, "⛽", T["avg_mileage"],     f"{mileage} km/L"),
                (sc2, "💰", T["total_fuel_cost"], f"₹{total_cost:,}"),
                (sc3, "📏", T["fuel_per_km"],     f"₹{cost_per_km}"),
            ]:
                with col:
                    st.markdown(f"""<div class="fuel-stat-box">
                        <div style="font-size:24px;">{icon}</div>
                        <div style="color:#8892b0;font-size:11px;margin-top:4px;">{label}</div>
                        <div style="color:#fff;font-weight:800;font-size:16px;margin-top:2px;">{val}</div>
                    </div>""", unsafe_allow_html=True)

            # Mileage trend mini-bars
            if len(fuel_log) >= 2:
                st.markdown("<div style='margin-top:16px;color:#8892b0;font-size:12px;font-weight:700;'>MILEAGE TREND</div>", unsafe_allow_html=True)
                max_l = max(e["liters"] for e in fuel_log)
                for e in fuel_log[:5]:
                    pct = int((e["liters"] / max_l) * 100)
                    cost_l = round(e["cost"] / e["liters"], 1)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:4px 0;">
                        <div style="min-width:45px;color:#8892b0;font-size:11px;">{e['date']}</div>
                        <div style="flex:1;background:#1e2240;border-radius:3px;height:8px;">
                            <div style="background:linear-gradient(90deg,#6c5ce7,#00c896);border-radius:3px;height:8px;width:{pct}%;"></div>
                        </div>
                        <div style="min-width:80px;font-size:11px;color:#cdd3f0;">{e['liters']}L @ ₹{cost_l}/L</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Fuel history table
        st.markdown(f'<div class="section-card"><div class="section-title">📋 {T["fuel_history"]}</div>', unsafe_allow_html=True)
        st.markdown("""<div style="display:grid;grid-template-columns:80px 70px 70px 100px;gap:4px;margin-bottom:6px;">
            <div style="color:#8892b0;font-size:11px;font-weight:700;">DATE</div>
            <div style="color:#8892b0;font-size:11px;font-weight:700;">LITERS</div>
            <div style="color:#8892b0;font-size:11px;font-weight:700;">COST</div>
            <div style="color:#8892b0;font-size:11px;font-weight:700;">ODOMETER</div>
        </div>""", unsafe_allow_html=True)
        for e in st.session_state.fuel_log:
            st.markdown(f"""<div class="log-row">
                <div style="min-width:80px;color:#cdd3f0;">{e['date']}</div>
                <div style="min-width:70px;color:#74c0fc;">{e['liters']} L</div>
                <div style="min-width:70px;color:#ff6b6b;">₹{e['cost']}</div>
                <div style="color:#8892b0;">{e['odometer']:,} km</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_expense:
        col_ef, col_eh = st.columns([1, 1])
        with col_ef:
            st.markdown(f'<div class="section-card"><div class="section-title">➕ {T["add_expense"]}</div>', unsafe_allow_html=True)
            with st.form("expense_form"):
                e_type   = st.selectbox(T["expense_type"], ["Parking", "Toll", "Car Wash", "Repair", "Food", "Mobile Recharge", "Other"])
                e_amount = st.number_input(T["expense_amount"], 5, 10000, 100, 5)
                e_note   = st.text_input(T["expense_note"], placeholder="e.g. Gandhipuram mall parking")
                e_date   = st.date_input("Date", value=now.date())
                e_submit = st.form_submit_button(f"➕ {T['expense_save']}", use_container_width=True)
                if e_submit:
                    st.session_state.expense_log.insert(0, {
                        "date":   e_date.strftime("%d %b"),
                        "type":   e_type,
                        "amount": e_amount,
                        "note":   e_note,
                    })
                    st.success("✅ Expense saved!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col_eh:
            # Expense by category
            exp_log = st.session_state.expense_log
            by_cat  = {}
            for e in exp_log:
                by_cat[e["type"]] = by_cat.get(e["type"], 0) + e["amount"]

            st.markdown(f'<div class="section-card"><div class="section-title">📊 Expense Breakdown</div>', unsafe_allow_html=True)
            total_exp = sum(by_cat.values()) if by_cat else 0
            for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
                pct = int((amt / max(total_exp, 1)) * 100)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;">
                        <span style="color:#cdd3f0;">{cat}</span>
                        <span style="color:#ffa94d;font-weight:700;">₹{amt}</span>
                    </div>
                    <div style="background:#1e2240;border-radius:4px;height:7px;">
                        <div style="background:#ffa94d;border-radius:4px;height:7px;width:{pct}%;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#8892b0;font-size:12px;margin-top:8px;'>Total: <b style='color:#ff6b6b;'>₹{total_exp}</b></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="section-card"><div class="section-title">📋 Expense Log</div>', unsafe_allow_html=True)
        for e in st.session_state.expense_log:
            st.markdown(f"""<div class="log-row">
                <div style="min-width:60px;color:#8892b0;font-size:12px;">{e['date']}</div>
                <div style="min-width:80px;color:#ffa94d;font-weight:600;">{e['type']}</div>
                <div style="flex:1;color:#cdd3f0;font-size:12px;">{e.get('note','—')}</div>
                <div style="color:#ff6b6b;font-weight:700;">₹{e['amount']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_summary:
        st.markdown(f"### 📊 {T['profit_loss']}")

        fuel_total   = sum(e["cost"]   for e in st.session_state.fuel_log)
        other_total  = sum(e["amount"] for e in st.session_state.expense_log)
        total_expense = fuel_total + other_total
        gross_earn   = today_earn
        commission   = round(gross_earn * 0.20)
        net_earn     = gross_earn - commission
        profit       = net_earn - total_expense
        profit_color = "#00c896" if profit > 0 else "#ff6b6b"

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Gross Earnings",   f"₹{gross_earn:,}")
        p2.metric("After Commission", f"₹{net_earn:,}", f"-₹{commission} (20%)")
        p3.metric("Total Expenses",   f"₹{total_expense:,}", f"Fuel ₹{fuel_total} + Other ₹{other_total}")
        p4.metric("Net Profit",       f"₹{profit:,}")

        # Visual P&L bar
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        rows_pl = [
            ("💰 Gross Earnings", gross_earn,   "#00c896", "+"),
            ("🏢 Commission",     commission,   "#ff6b6b", "-"),
            ("⛽ Fuel Cost",      fuel_total,   "#ffa94d", "-"),
            ("💸 Other Expenses", other_total,  "#ff6b6b", "-"),
            ("✅ Net Profit",     abs(profit),  profit_color, "=" if profit > 0 else "= -"),
        ]
        max_val = max(abs(r[1]) for r in rows_pl) or 1
        for label, val, clr, sign in rows_pl:
            pct = int((abs(val) / max_val) * 100)
            sep = "border-top:2px solid #6c5ce7;padding-top:10px;margin-top:6px;" if "Net" in label else ""
            st.markdown(f"""
            <div style="margin-bottom:8px;{sep}">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                    <span style="color:#cdd3f0;font-weight:{'700' if 'Net' in label else '400'};">{label}</span>
                    <span style="color:{clr};font-weight:700;">{sign}₹{val:,}</span>
                </div>
                <div style="background:#1e2240;border-radius:4px;height:8px;">
                    <div style="background:{clr};border-radius:4px;height:8px;width:{pct}%;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Tips based on expenses
        if fuel_total > net_earn * 0.3:
            st.warning("⚠️ Fuel cost is >30% of your earnings. Consider switching to a fuel-efficient route or adjusting zones.")
        else:
            st.success("✅ Fuel efficiency looks healthy — under 30% of earnings.")

# ════════════════════════════════════════════════════════════════════════════
# ── VEHICLE MAINTENANCE ────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_maintenance"]:
    st.markdown(f"### 🔧 {T['maint_title']}")

    tab_health, tab_schedule, tab_log = st.tabs(["🩺 Vehicle Health", "📅 Schedule", "📋 Service Log"])

    with tab_health:
        current_odo = st.session_state.current_odometer
        last_svc_odo = st.session_state.last_service_odometer

        # Compute health score
        items_due   = 0
        items_ok    = 0
        items_overdue = 0
        statuses    = {}
        for m in MAINTENANCE_ITEMS:
            last_odo = last_svc_odo.get(m["name"], current_odo - m["interval_km"] - 500)
            km_since = current_odo - last_odo
            km_left  = m["interval_km"] - km_since
            if km_left < 0:
                statuses[m["name"]] = ("overdue", abs(km_left))
                items_overdue += 1
            elif km_left < m["interval_km"] * 0.2:
                statuses[m["name"]] = ("due_soon", km_left)
                items_due += 1
            else:
                statuses[m["name"]] = ("good", km_left)
                items_ok += 1

        total_items  = len(MAINTENANCE_ITEMS)
        health_score = int(((items_ok + items_due * 0.5) / total_items) * 100)
        h_color      = score_color(health_score)

        col_ring, col_stats = st.columns([1, 2])
        with col_ring:
            st.markdown(f"""
            <div style="text-align:center;padding:20px 0;">
                <div style="width:130px;height:130px;border-radius:50%;
                     background: conic-gradient({h_color} {health_score}%, #1e2240 {health_score}%);
                     display:flex;align-items:center;justify-content:center;margin:0 auto;
                     box-shadow: 0 0 20px {h_color}40;">
                    <div style="width:90px;height:90px;border-radius:50%;background:#0d0f1a;
                         display:flex;flex-direction:column;align-items:center;justify-content:center;">
                        <div style="font-size:26px;font-weight:900;color:{h_color};">{health_score}</div>
                        <div style="font-size:10px;color:#8892b0;">/ 100</div>
                    </div>
                </div>
                <div style="margin-top:12px;font-size:14px;font-weight:700;color:{h_color};">{T['vehicle_health']}</div>
            </div>""", unsafe_allow_html=True)

        with col_stats:
            st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
            for icon, count, label, clr in [
                ("✅", items_ok,      f"Items {T['good']}",    "#00c896"),
                ("⚠️", items_due,     T["due_soon"],           "#ffa94d"),
                ("🔴", items_overdue, T["overdue"],            "#ff6b6b"),
            ]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #1e2240;">
                    <div style="font-size:20px;">{icon}</div>
                    <div style="flex:1;font-size:14px;color:#cdd3f0;">{label}</div>
                    <div style="font-size:22px;font-weight:800;color:{clr};">{count}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-top:10px;font-size:12px;color:#8892b0;">
                📍 Current Odometer: <b style="color:#cdd3f0;">{current_odo:,} km</b>
            </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Overdue alerts
        overdue_items = [m for m in MAINTENANCE_ITEMS if statuses.get(m["name"], ("good",))[0] == "overdue"]
        if overdue_items:
            st.error(f"🚨 {len(overdue_items)} maintenance item(s) are OVERDUE! Service immediately to avoid breakdowns.")
            for m in overdue_items:
                km_over = statuses[m["name"]][1]
                st.markdown(f"- **{m['icon']} {m['name']}** — overdue by {km_over:,} km (est. cost: ₹{m['cost_est']})")

    with tab_schedule:
        st.markdown(f'<div class="section-card"><div class="section-title">📅 {T["maint_schedule"]}</div>', unsafe_allow_html=True)
        current_odo = st.session_state.current_odometer
        last_svc_odo = st.session_state.last_service_odometer

        for m in MAINTENANCE_ITEMS:
            last_odo = last_svc_odo.get(m["name"], current_odo - m["interval_km"] + 1000)
            km_since = current_odo - last_odo
            km_left  = m["interval_km"] - km_since
            status, val = statuses.get(m["name"], ("good", km_left))

            if status == "overdue":
                border_clr = "#ff6b6b"; bg = "#1a0000"; status_txt = f"⛔ {T['overdue']} by {abs(val):,} km"
            elif status == "due_soon":
                border_clr = "#ffa94d"; bg = "#1a1200"; status_txt = f"⚠️ {T['due_soon']}: {val:,.0f} km left"
            else:
                border_clr = "#00c896"; bg = "#001a10"; status_txt = f"✅ {T['good']}: {val:,.0f} km left"

            pct = max(0, min(100, int((km_since / m["interval_km"]) * 100)))
            bar_clr = "#ff6b6b" if status == "overdue" else "#ffa94d" if status == "due_soon" else "#00c896"

            st.markdown(f"""
            <div style="background:{bg};border-left:4px solid {border_clr};border-radius:10px;
                        padding:14px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:15px;font-weight:700;color:#fff;">{m['icon']} {m['name']}</div>
                        <div style="font-size:11px;color:#8892b0;margin-top:2px;">Every {m['interval_km']:,} km · Est. ₹{m['cost_est']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:12px;color:{border_clr};font-weight:700;">{status_txt}</div>
                    </div>
                </div>
                <div style="background:#1e2240;border-radius:4px;height:6px;margin-top:10px;">
                    <div style="background:{bar_clr};border-radius:4px;height:6px;width:{pct}%;"></div>
                </div>
                <div style="font-size:11px;color:#8892b0;margin-top:4px;">{km_since:,} / {m['interval_km']:,} km used</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_log:
        col_form, col_hist = st.columns([1, 1])
        with col_form:
            st.markdown(f'<div class="section-card"><div class="section-title">➕ {T["add_service"]}</div>', unsafe_allow_html=True)
            with st.form("service_form"):
                svc_type = st.selectbox(T["service_type"], [m["name"] for m in MAINTENANCE_ITEMS] + ["Other"])
                svc_date = st.date_input(T["service_date"], value=now.date())
                s_col1, s_col2 = st.columns(2)
                svc_cost = s_col1.number_input(T["service_cost"], 0, 20000, 800, 50)
                svc_odo  = s_col2.number_input(T["fuel_odometer"], 0, 999999, st.session_state.current_odometer, 10)
                svc_note = st.text_area(T["service_notes"], placeholder="e.g. Used 5W-30 synthetic oil", height=80)
                svc_save = st.form_submit_button(f"💾 {T['service_save']}", use_container_width=True)
                if svc_save:
                    st.session_state.service_log.insert(0, {
                        "date":      svc_date.strftime("%d %b %Y"),
                        "type":      svc_type,
                        "cost":      svc_cost,
                        "odometer":  svc_odo,
                        "notes":     svc_note,
                    })
                    if svc_type in st.session_state.last_service_odometer:
                        st.session_state.last_service_odometer[svc_type] = svc_odo
                    st.success(f"✅ {svc_type} service logged!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col_hist:
            total_svc_cost = sum(s["cost"] for s in st.session_state.service_log)
            st.markdown(f'<div class="section-card"><div class="section-title">📋 {T["maint_history"]}</div>', unsafe_allow_html=True)
            for s in st.session_state.service_log:
                st.markdown(f"""
                <div style="padding:10px 0;border-bottom:1px solid #1e2240;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:14px;font-weight:600;color:#cdd3f0;">🔧 {s['type']}</div>
                            <div style="font-size:11px;color:#8892b0;">{s['date']} · {s['odometer']:,} km</div>
                            {f'<div style="font-size:11px;color:#8892b0;margin-top:2px;">{s["notes"]}</div>' if s.get("notes") else ""}
                        </div>
                        <div style="color:#ff6b6b;font-weight:700;">₹{s['cost']:,}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:10px;color:#8892b0;font-size:13px;'>Total service cost: <b style='color:#ff6b6b;'>₹{total_svc_cost:,}</b></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ── SAFETY & SOS ──────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_safety"]:
    st.markdown(f"### 🛡️ {T['safety_title']}")

    tab_sos, tab_contacts, tab_checklist, tab_incident = st.tabs([
        "🚨 SOS", "👥 Contacts", "✅ Checklist", "📝 Report Incident"
    ])

    with tab_sos:
        col_sos, col_score = st.columns([2, 1])

        with col_sos:
            # SOS card
            sos_status = st.session_state.sos_active
            sos_bg     = "#3d0000" if not sos_status else "#001a00"
            sos_border = "#ff3333" if not sos_status else "#00c896"
            sos_icon   = "🚨" if not sos_status else "✅"

            st.markdown(f"""
            <div style="background:{sos_bg};border:2px solid {sos_border};border-radius:16px;
                        padding:28px;text-align:center;margin-bottom:16px;
                        box-shadow:0 0 30px {sos_border}33;">
                <div style="font-size:48px;margin-bottom:8px;">{sos_icon}</div>
                <div style="font-size:20px;font-weight:900;color:#fff;margin-bottom:8px;">{T['sos_title']}</div>
                <div style="font-size:13px;color:#8892b0;margin-bottom:16px;">{T['sos_desc']}</div>
            </div>""", unsafe_allow_html=True)

            sos_active = st.session_state.sos_active
            if not sos_active:
                if st.button(f"🚨 {T['sos_btn']}", use_container_width=True, type="primary"):
                    st.session_state.sos_active = True
                    st.rerun()
            else:
                st.error(f"**{T['sos_sent']}**")
                st.markdown("""
                <div style="background:#001a00;border:1px solid #00c896;border-radius:12px;padding:16px;margin:8px 0;">
                    <div style="color:#00c896;font-weight:700;font-size:14px;margin-bottom:8px;">📡 Alert Sent To:</div>
                    <div style="color:#cdd3f0;font-size:13px;line-height:2;">
                        ✅ Platform Emergency Team<br>
                        ✅ Emergency Contact #1<br>
                        ✅ Local Police (112)<br>
                        📍 Your live location is being shared
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button("✅ I'm Safe — Cancel SOS", use_container_width=True):
                    st.session_state.sos_active = False
                    st.rerun()

            # Safe Check-In
            st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="section-card"><div class="section-title">🟢 Safety Check-In</div>', unsafe_allow_html=True)
            last_ci = st.session_state.last_checkin
            if last_ci:
                diff = datetime.now() - last_ci
                mins = int(diff.total_seconds() / 60)
                checkin_color = "#00c896" if mins < 60 else "#ffa94d" if mins < 120 else "#ff6b6b"
                st.markdown(f"<div style='color:#8892b0;font-size:13px;margin-bottom:8px;'>{T['last_checkin']}: <b style='color:{checkin_color};'>{mins} mins ago</b></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#8892b0;font-size:13px;margin-bottom:8px;'>No check-in yet today.</div>", unsafe_allow_html=True)

            if st.button(f"{T['checkin_btn']}", use_container_width=True):
                st.session_state.last_checkin = datetime.now()
                st.success(f"✅ Check-in recorded at {datetime.now().strftime('%I:%M %p')}")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            # Night mode toggle
            st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
            col_nm1, col_nm2 = st.columns([2, 1])
            with col_nm1:
                st.markdown(f"""
                <div>
                    <div style="font-weight:700;color:#cdd3f0;font-size:14px;">🌙 {T['night_mode']}</div>
                    <div style="color:#8892b0;font-size:12px;margin-top:4px;">{T['night_mode_desc']}</div>
                </div>""", unsafe_allow_html=True)
            with col_nm2:
                night_toggle = st.toggle("Enable", value=st.session_state.night_mode, key="nm_toggle")
                if night_toggle != st.session_state.night_mode:
                    st.session_state.night_mode = night_toggle
                    st.rerun()
            if st.session_state.night_mode:
                st.success("🌙 Night Safety Mode is ACTIVE — location auto-shared every 30 mins.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_score:
            # Safety score
            safety_score = 88 if not st.session_state.sos_active else 65
            sc = score_color(safety_score)
            st.markdown(f"""
            <div style="background:#1a1f3a;border-radius:14px;padding:20px;border:1px solid #2a2f50;text-align:center;margin-bottom:16px;">
                <div style="font-size:13px;font-weight:700;color:#8892b0;margin-bottom:12px;">{T['safety_score']}</div>
                <div style="width:100px;height:100px;border-radius:50%;
                     background:conic-gradient({sc} {safety_score}%, #1e2240 {safety_score}%);
                     display:flex;align-items:center;justify-content:center;margin:0 auto;">
                    <div style="width:70px;height:70px;border-radius:50%;background:#1a1f3a;
                         display:flex;flex-direction:column;align-items:center;justify-content:center;">
                        <div style="font-size:22px;font-weight:900;color:{sc};">{safety_score}</div>
                        <div style="font-size:9px;color:#8892b0;">/ 100</div>
                    </div>
                </div>
                <div style="margin-top:14px;font-size:12px;color:#8892b0;line-height:1.8;">
                    <div>✅ Acceptance Rate: 94%</div>
                    <div>✅ No incidents (30 days)</div>
                    <div>✅ Night mode: {'ON' if st.session_state.night_mode else 'OFF'}</div>
                    <div>⭐ Rating: 4.8</div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Safe zones display
            st.markdown(f'<div class="section-card"><div class="section-title">🛡️ {T["safe_zones"]}</div>', unsafe_allow_html=True)
            for z, zi in ZONES_INFO.items():
                safe_clr  = "#00c896" if zi["safe"] else "#ff6b6b"
                safe_icon = "✅" if zi["safe"] else "⚠️"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #1e2240;">
                    <span>{zi['icon']}</span>
                    <span style="color:#cdd3f0;font-size:13px;flex:1;">Zone {z} – {zi['name']}</span>
                    <span style="color:{safe_clr};font-size:12px;font-weight:700;">{safe_icon}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_contacts:
        col_cf, col_cl = st.columns([1, 1])

        with col_cf:
            st.markdown(f'<div class="section-card"><div class="section-title">➕ {T["add_contact"]}</div>', unsafe_allow_html=True)
            with st.form("contact_form"):
                c_name     = st.text_input(T["contact_name"],     placeholder="Priya Kumar")
                c_phone    = st.text_input(T["contact_phone"],    placeholder="9876543210")
                c_relation = st.selectbox(T["contact_relation"],  ["Spouse","Parent","Sibling","Friend","Other"])
                c_save     = st.form_submit_button(f"💾 {T['contact_save']}", use_container_width=True)
                if c_save:
                    if c_name and c_phone:
                        st.session_state.emergency_contacts.append({
                            "name": c_name, "phone": c_phone, "relation": c_relation
                        })
                        st.success(f"✅ {c_name} added as emergency contact!")
                        st.rerun()
                    else:
                        st.error("Please fill name and phone.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_cl:
            st.markdown(f'<div class="section-card"><div class="section-title">👥 {T["safety_contacts"]}</div>', unsafe_allow_html=True)
            contacts = st.session_state.emergency_contacts
            if not contacts:
                st.markdown("<div style='color:#8892b0;font-size:13px;padding:8px 0;'>No contacts added yet.</div>", unsafe_allow_html=True)
            for i, c in enumerate(contacts):
                st.markdown(f"""
                <div style="background:#1e2240;border-radius:10px;padding:14px;margin-bottom:8px;
                            border-left:3px solid #6c5ce7;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:700;color:#fff;font-size:14px;">{c['name']}</div>
                            <div style="color:#8892b0;font-size:12px;">{c['relation']} · 📱 {c['phone']}</div>
                        </div>
                        <div style="color:#00c896;font-size:20px;">👤</div>
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"🗑️ Remove {c['name']}", key=f"del_contact_{i}"):
                    st.session_state.emergency_contacts.pop(i)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Platform emergency numbers
        st.markdown(f'<div class="section-card"><div class="section-title">📞 Emergency Numbers</div>', unsafe_allow_html=True)
        numbers = [
            ("🚓", "Police",              "100"),
            ("🚑", "Ambulance",           "108"),
            ("🔥", "Fire",                "101"),
            ("📞", "Women Helpline",      "1091"),
            ("🏥", "Govt Hospital CBE",   "0422-2301234"),
            ("🚗", "Platform Support",    "1800-XXX-XXXX"),
        ]
        for icon, label, num in numbers:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1e2240;">
                <div style="font-size:13px;color:#cdd3f0;">{icon} {label}</div>
                <div style="font-size:14px;font-weight:700;color:#74c0fc;">{num}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_checklist:
        st.markdown(f"#### ✅ {T['safety_checklist']}")
        checklist_items = {
            "en": [
                ("🚗", "Vehicle documents ready (RC, insurance, licence)"),
                ("⛽", "Fuel is sufficient for the day"),
                ("📱", "Phone fully charged"),
                ("🔦", "Emergency torch / flashlight available"),
                ("🏥", "First aid kit in vehicle"),
                ("💧", "Water bottle for long shifts"),
                ("📷", "Dashcam is working"),
                ("🔒", "Doors lock/unlock properly"),
                ("💺", "Seat belts functional"),
                ("🪪", "Driver ID badge visible"),
            ],
        }
        items = checklist_items["en"]
        checked_count = 0
        for idx, (icon, label) in enumerate(items):
            key  = f"chk_{idx}"
            val  = st.session_state.safety_checklist.get(key, False)
            chkd = st.checkbox(f"{icon} {label}", value=val, key=f"cb_{key}")
            st.session_state.safety_checklist[key] = chkd
            if chkd:
                checked_count += 1

        pct = int((checked_count / len(items)) * 100)
        clr = "#00c896" if pct >= 80 else "#ffa94d" if pct >= 50 else "#ff6b6b"
        st.markdown(f"""
        <div style="margin-top:16px;background:#1a1f3a;border-radius:12px;padding:16px;border:1px solid #2a2f50;">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#cdd3f0;font-weight:700;">Safety Checklist Progress</span>
                <span style="color:{clr};font-weight:800;">{checked_count}/{len(items)}</span>
            </div>
            <div style="background:#1e2240;border-radius:6px;height:12px;">
                <div style="background:{clr};border-radius:6px;height:12px;width:{pct}%;transition:width 0.5s;"></div>
            </div>
            <div style="color:{clr};font-size:12px;margin-top:6px;">
                {'✅ You are road-ready!' if pct == 100 else f'{100-pct}% remaining — check all items before starting.'}
            </div>
        </div>""", unsafe_allow_html=True)

    with tab_incident:
        st.markdown(f"#### 📝 {T['incident_report']}")
        col_if, col_ih = st.columns([1, 1])

        with col_if:
            with st.form("incident_form"):
                i_type = st.selectbox(T["incident_type"], [
                    "Aggressive Passenger", "Route Dispute", "Payment Issue",
                    "Accident / Collision", "Vehicle Breakdown", "Harassment",
                    "Suspicious Behaviour", "Other"
                ])
                i_zone = st.selectbox(T["incident_zone"], [f"Zone {z} – {ZONES_INFO[z]['name']}" for z in ZONES_INFO])
                i_time = st.text_input(T["incident_time"], value=now.strftime("%I:%M %p"))
                i_desc = st.text_area(T["incident_desc"], placeholder="Describe what happened...", height=120)
                i_sub  = st.form_submit_button(f"📤 {T['incident_submit']}", use_container_width=True)
                if i_sub:
                    if i_desc:
                        st.session_state.incident_reports.insert(0, {
                            "type":  i_type,
                            "zone":  i_zone,
                            "time":  i_time,
                            "desc":  i_desc,
                            "date":  now.strftime("%d %b %Y"),
                        })
                        st.success("✅ Incident reported. Platform team will review within 24 hours.")
                        st.rerun()
                    else:
                        st.error("Please describe the incident.")

        with col_ih:
            st.markdown(f'<div class="section-card"><div class="section-title">📋 Incident History</div>', unsafe_allow_html=True)
            reports = st.session_state.incident_reports
            if not reports:
                st.markdown("<div style='color:#8892b0;font-size:13px;padding:8px;'>No incidents reported. Stay safe! 🛡️</div>", unsafe_allow_html=True)
            for r in reports:
                type_colors = {
                    "Accident / Collision": "#ff3333",
                    "Aggressive Passenger": "#ff6b6b",
                    "Harassment": "#ff6b6b",
                    "Payment Issue": "#ffa94d",
                    "Vehicle Breakdown": "#ffa94d",
                    "Route Dispute": "#ffa94d",
                }
                r_clr = type_colors.get(r["type"], "#74c0fc")
                st.markdown(f"""
                <div style="background:#1e2240;border-radius:10px;padding:12px;margin-bottom:8px;
                            border-left:3px solid {r_clr};">
                    <div style="display:flex;justify-content:space-between;">
                        <div style="font-weight:700;color:{r_clr};font-size:13px;">{r['type']}</div>
                        <div style="color:#8892b0;font-size:11px;">{r['date']}</div>
                    </div>
                    <div style="color:#8892b0;font-size:11px;margin-top:2px;">{r['zone']} · {r['time']}</div>
                    <div style="color:#cdd3f0;font-size:12px;margin-top:4px;line-height:1.5;">{r['desc'][:120]}{'...' if len(r['desc'])>120 else ''}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ── SETTINGS ──────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
elif page == T["nav_settings"]:
    st.markdown(f"### ⚙️ {T['nav_settings']}")

    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🔔 Notifications", "🚗 Vehicle Info", "ℹ️ About"])

    with tab1:
        st.subheader("Driver Profile")
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("Full Name", st.session_state.driver_name)
            new_veh  = st.text_input("Vehicle Number", st.session_state.vehicle_no)
        with c2:
            st.text_input("Phone", "98765XXXXX")
            st.selectbox("Vehicle Type", ["Auto Rickshaw","Bike Taxi","Car (Mini)","Car (Sedan)","Car (SUV)"])
        if st.button("💾 Save Profile", use_container_width=True):
            st.session_state.driver_name = new_name
            st.session_state.vehicle_no  = new_veh
            st.success("✅ Profile saved!")
        st.subheader("Language Preference")
        lang_opt = st.selectbox("App Language", ["English","தமிழ்","हिंदी","ಕನ್ನಡ"],
                                 index=["English","தமிழ்","हिंदी","ಕನ್ನಡ"].index(st.session_state.lang))
        if st.button("🌐 Apply Language"):
            st.session_state.lang = lang_opt
            st.rerun()

    with tab2:
        st.subheader("Notification Settings")
        st.checkbox("🔥 High demand zone alerts", value=True)
        st.checkbox("🎁 Bonus eligibility alerts", value=True)
        st.checkbox("⛽ Low fuel reminder", value=True)
        st.checkbox("🔧 Maintenance due reminders", value=True)
        st.checkbox("🌙 Night safety check-in (10 PM)", value=True)
        st.checkbox("📈 Daily earnings summary", value=True)
        st.checkbox("🗺 Zone switch recommendations", value=True)
        st.checkbox("🚨 SOS auto-alert after 2 mins no response", value=False)
        if st.button("Save Notifications"):
            st.success("✅ Notification preferences saved!")

    with tab3:
        st.subheader("Vehicle Information")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Vehicle Make", placeholder="Maruti / Hyundai / Honda")
            st.text_input("Model", placeholder="Swift / WagonR / Alto")
            st.text_input("Year", placeholder="2020")
        with c2:
            st.number_input("Current Odometer (km)", value=st.session_state.current_odometer, step=10, key="odo_settings")
            st.text_input("Insurance Expiry", placeholder="DD/MM/YYYY")
            st.text_input("PUC Expiry", placeholder="DD/MM/YYYY")
        if st.button("💾 Save Vehicle Info"):
            st.session_state.current_odometer = st.session_state.odo_settings
            st.success("✅ Vehicle info saved!")

    with tab4:
        st.markdown("""
        <div style="background:#1a1f3a;border-radius:12px;padding:20px;border:1px solid #2a2f50;">
            <div style="font-size:15px;color:#cdd3f0;line-height:1.9;">
                <b style="color:#fff;">🚗 Driver AI Copilot v3.0</b><br><br>
                <b style="color:#a29bfe;">What's new in v3:</b><br>
                • ⛽ Fuel & Expense Tracker with P&L summary<br>
                • 🔧 Vehicle Maintenance scheduler with health score<br>
                • 🚨 Enhanced SOS with live location sharing<br>
                • ✅ Daily safety checklist<br>
                • 👥 Multi-contact emergency system<br>
                • 📝 Incident reporting with history<br>
                • 🌙 Night safety auto-mode<br>
                • 🛡️ Safe zone indicators on heatmap<br><br>
                <b style="color:#a29bfe;">All Features:</b><br>
                • Real-time demand across 4 Coimbatore zones<br>
                • AI assistant powered by Claude (Anthropic)<br>
                • Earnings predictions & fare calculator<br>
                • 4-language support (EN / Tamil / Hindi / Kannada)<br>
                • Google Maps deep-link navigation<br><br>
                <b style="color:#a29bfe;">Version:</b> 3.0 — Safety + Expense Edition<br>
                <b style="color:#a29bfe;">Team:</b> THE AI ACES
            </div>
        </div>""", unsafe_allow_html=True)