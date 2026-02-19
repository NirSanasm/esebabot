from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json
import re
from datetime import datetime

app = FastAPI(title="e-Seba Manipur Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Knowledge Base ───────────────────────────────────────────────────────────

KNOWLEDGE_BASE =[
  {
    "id": "landing_page_001",
    "service": "General",
    "category": "Navigation",
    "question": "What options are available on the e-Seba Manipur landing page?",
    "answer": "The e-Seba Manipur landing page has a top navigation bar with: HOME, APPLICATION STATUS, CERTIFICATE DOWNLOAD, CONTACT US, and LOGIN. The hero section has two main action buttons: 'Citizen Services - Register & Apply' (blue button) for new users or starting a new application, and 'Track Application Status' (outlined button) to check pending applications without logging in.",
    "keywords": [
      "landing page",
      "navigation",
      "home",
      "eseba",
      "manipur",
      "menu"
    ]
  },
  {
    "id": "landing_page_002",
    "service": "General",
    "category": "Navigation",
    "question": "How can I track my application status without logging in?",
    "answer": "You can track your application status without logging in by clicking the 'Track Application Status' button on the landing page hero section, or by clicking 'APPLICATION STATUS' in the top navigation bar.",
    "keywords": [
      "track",
      "application status",
      "without login",
      "guest",
      "check status"
    ]
  },
  {
    "id": "landing_page_003",
    "service": "General",
    "category": "Navigation",
    "question": "How do I download a certificate from e-Seba Manipur?",
    "answer": "You can download approved certificates by clicking 'CERTIFICATE DOWNLOAD' in the top navigation bar on the landing page.",
    "keywords": [
      "certificate download",
      "download",
      "approved certificate",
      "navigation"
    ]
  },


    {
    "id": "login_000",
    "service": "Login",
    "category": "Overview",
    "question": "about login?",
    "answer": "In this login section, you can find info about the login methods available on e-Seba Manipur, including Mobile OTP and Username/Password login. It also explains the captcha security feature and provides step-by-step instructions for both login methods.",
    "keywords": [
      "login",
      "mobile OTP",
      "username",
      "password",
      "sign in"
    ]
  },

  {
    "id": "login_001",
    "service": "Login",
    "category": "Login",
    "question": "What are the login methods available on e-Seba Manipur?",
    "answer": "e-Seba Manipur offers two login methods: (1) Mobile OTP – login using your registered mobile number and a One-Time Password sent via SMS, and (2) Username – login using the username and password you created during registration.",
    "keywords": [
      "login",
      "mobile OTP",
      "username",
      "password",
      "sign in"
    ]
  },
  {
    "id": "login_002",
    "service": "Login",
    "category": "Login",
    "question": "How do I log in using my mobile number on e-Seba Manipur?",
    "answer": "To log in using your mobile number: (1) Go to the Login page, (2) Select the 'Mobile OTP' tab, (3) Enter your registered 10-digit mobile number, (4) Solve the captcha math problem, (5) Click 'Send OTP', (6) Enter the 6-digit OTP received via SMS, and (7) Submit to log in.",
    "keywords": [
      "mobile OTP",
      "login",
      "OTP",
      "mobile number",
      "sign in"
    ]
  },
  {
    "id": "login_003",
    "service": "Login",
    "category": "Login",
    "question": "How do I log in using my username and password?",
    "answer": "To log in with username and password: (1) Go to the Login page, (2) Select the 'Username' tab, (3) Enter your registered username, (4) Enter your password, (5) Solve the captcha math problem, and (6) Click the 'Login' button.",
    "keywords": [
      "username",
      "password",
      "login",
      "sign in",
      "credentials"
    ]
  },
  {
    "id": "login_004",
    "service": "Login",
    "category": "Login",
    "question": "What is the captcha on the login page?",
    "answer": "The captcha on the e-Seba Manipur login page is a simple math challenge (e.g., '1 + 7 = ?'). You need to solve the math problem and enter the answer in the provided field. This is a security measure to prevent automated bot attacks.",
    "keywords": [
      "captcha",
      "math",
      "security",
      "login",
      "bot prevention"
    ]
  },

   {
    "id": "registration_000",
    "service": "New Registration",
    "category": "Overview",
    "question": "About Registration?",
    "answer": "In this registration section, you can find detailed information about the new registration process on e-Seba Manipur. It covers the step-by-step procedure to create a new account, the personal details required, the credentials you need to set, and important tips for successful registration.",
    "keywords": [
      "register",
      "new account",
      "sign up",
      "create account",
      "registration"
    ]
  },

  {
    "id": "registration_001",
    "service": "New Registration",
    "category": "Registration",
    "question": "How do I register a new account on e-Seba Manipur?",
    "answer": "To register a new account: (1) Go to the login page, (2) Click 'Don't have an account? Register here', (3) Enter your 10-digit mobile number and solve the captcha, (4) Click 'Send OTP', (5) Enter the 6-digit OTP and click 'Verify OTP', (6) Fill in your personal details form, and (7) Set your username, password, and address details, then click 'Next' to complete registration.",
    "keywords": [
      "register",
      "new account",
      "sign up",
      "create account",
      "registration"
    ]
  },
  {
    "id": "registration_002",
    "service": "New Registration",
    "category": "Registration",
    "question": "What is the first step in the registration process?",
    "answer": "The first step in registration is Mobile Verification. You must enter a valid 10-digit mobile number, solve the captcha math problem, and click 'Send OTP'. A 6-digit verification code will be sent to your mobile number.",
    "keywords": [
      "registration",
      "first step",
      "mobile verification",
      "OTP",
      "mobile number"
    ]
  },
  {
    "id": "registration_003",
    "service": "New Registration",
    "category": "Registration",
    "question": "What personal details are required during registration?",
    "answer": "Mandatory personal details required during registration include: First Name, Last Name, Email address, Date of Birth, Gender, Marital Status, Citizen/CSC type, Name as per Aadhaar, Aadhaar Number (12-digit), Father's Name, Mother's Name, Caste Category, Religion, and Area. Optional fields include Middle Name and Spouse Name (if married).",
    "keywords": [
      "registration",
      "personal details",
      "required fields",
      "mandatory",
      "aadhaar",
      "name"
    ]
  },
  {
    "id": "registration_004",
    "service": "New Registration",
    "category": "Registration",
    "question": "What credentials do I need to create during registration?",
    "answer": "During registration, you need to create a unique Username (which you'll use to log in) and a Password. The password field has an eye icon to toggle visibility. These credentials are set in the 'Credential Details' section of the registration form.",
    "keywords": [
      "username",
      "password",
      "credentials",
      "registration",
      "create account"
    ]
  },
  {
    "id": "registration_005",
    "service": "New Registration",
    "category": "Registration",
    "question": "Do I need to enter both present and permanent address during registration?",
    "answer": "Yes, both Present Address and Permanent Address are required during registration. However, if your present and permanent addresses are the same, you can check the 'Present address is same as Permanent' checkbox to automatically copy the present address fields to the permanent address section, saving time.",
    "keywords": [
      "address",
      "present address",
      "permanent address",
      "registration",
      "same address",
      "checkbox"
    ]
  },
  {
    "id": "registration_006",
    "service": "New Registration",
    "category": "Registration",
    "question": "What happens after I verify my OTP during registration?",
    "answer": "After successfully verifying your OTP, you are directed to the detailed registration form (Step 3: Personal Details Form) where you fill in your demographic and identity information including name, email, date of birth, gender, Aadhaar details, and other personal information.",
    "keywords": [
      "OTP",
      "verified",
      "after OTP",
      "registration",
      "next step",
      "personal details"
    ]
  },
  {
    "id": "registration_007",
    "service": "New Registration",
    "category": "Registration",
    "question": "What if I don't receive the OTP during registration?",
    "answer": "If you don't receive the OTP, you can click the 'Resent OTP' link on the OTP confirmation screen to request a new verification code. Make sure the mobile number you entered is correct and active.",
    "keywords": [
      "resend OTP",
      "OTP not received",
      "registration",
      "OTP expired",
      "new OTP"
    ]
  },
  {
    "id": "registration_008",
    "service": "New Registration",
    "category": "Registration",
    "question": "What address fields are required during registration?",
    "answer": "For both Present and Permanent Address, the following fields are required: Address (house/street), City/Town, District, Pincode, Post Office, and Police Station.",
    "keywords": [
      "address fields",
      "registration",
      "city",
      "district",
      "pincode",
      "post office",
      "police station"
    ]
  },

  
  {
    "id": "dashboard_001",
    "service": "General",
    "category": "Dashboard",
    "question": "What can I do from the user dashboard on e-Seba Manipur?",
    "answer": "From the user dashboard you can: Apply for government services, view your applied, pending, issued, and rejected applications, change your password, edit or view your profile, track application status, download certificates, and see a summary of all your application counts and recent activity.",
    "keywords": [
      "dashboard",
      "features",
      "overview",
      "what can I do",
      "home page"
    ]
  },
  {
    "id": "dashboard_002",
    "service": "General",
    "category": "Dashboard",
    "question": "What KPI cards are shown on the dashboard?",
    "answer": "The dashboard displays four KPI cards: (1) Total Applications – count of all applications ever started, (2) Saved Drafts – incomplete applications that can be resumed, (3) Submitted – applications sent for processing, and (4) Issued – completed requests where certificates have been generated.",
    "keywords": [
      "KPI",
      "dashboard cards",
      "total applications",
      "drafts",
      "submitted",
      "issued"
    ]
  },
  {
    "id": "dashboard_003",
    "service": "General",
    "category": "Dashboard",
    "question": "What are the sidebar menu options on the dashboard?",
    "answer": "The sidebar menu includes: Dashboard (main view), Apply Services (browse available services), Applications (with sub-options: Applied List, Pending List, Issued List, Rejected List), Account (with sub-options: Change Password, Edit Profile, View Profile), and Logout.",
    "keywords": [
      "sidebar",
      "menu",
      "navigation",
      "dashboard",
      "options"
    ]
  },
  {
    "id": "dashboard_004",
    "service": "General",
    "category": "Dashboard",
    "question": "What is the 'Pending List' in my dashboard?",
    "answer": "The 'Pending List' under Applications in your dashboard shows all your applications that are currently waiting for government action or processing. These are applications you have submitted but have not yet been approved, issued, or rejected.",
    "keywords": [
      "pending list",
      "pending applications",
      "waiting",
      "government action",
      "dashboard"
    ]
  },
  {
    "id": "dashboard_005",
    "service": "General",
    "category": "Dashboard",
    "question": "How do I start a new application from the dashboard?",
    "answer": "You can start a new application in two ways from the dashboard: (1) Click 'Apply Services' in the sidebar menu to browse all available government services, or (2) Use the 'New Application' quick action button in the main content area.",
    "keywords": [
      "new application",
      "apply services",
      "start application",
      "dashboard",
      "quick action"
    ]
  },
  {
    "id": "employment_000",
    "service": "Employment Exchange",
    "category": "Overview",
    "question": "What is the Employment Exchange Registration service on e-Seba Manipur?",
    "answer": "The Employment Exchange Registration service on e-Seba Manipur allows citizens to register as job seekers. E seba provides five types of Employment Exchange services namely Registration in Employment Exchange, Renewal of Employment Exchange Registration, Application against vacancy, Transfer of registration to employment exchange, Updating qualification or experience. Users can also do Job Seeker Profile Update, Job Seeker Profile View, and Employment Exchange Certificate Download. Through this service, you can store your qualifications, work experience, and job preferences, upload required documents, and submit an application to the Employment Exchange. After submission, you can track your application status and download an acknowledgement receipt.",
    "keywords": [
      "employment exchange",
      "registration",
      "job seeker",
      "employment",
      "e-seba"
    ]
  },
  {
    "id": "employment_002",
    "service": "Employment Exchange",
    "category": "Navigation",
    "question": "How do I navigate to the Employment Exchange Registration on e-Seba Manipur?",
    "answer": "To reach the Employment Exchange Registration: (1) Log in and go to your Dashboard, (2) Click 'Apply Services' in the sidebar, (3) Choose 'Employment Exchange', (4) Select 'Registration in Employment Exchange', and (5) Click 'New Registration'.",
    "keywords": [
      "how to navigate",
      "employment exchange",
      "find service",
      "apply services",
      "new registration"
    ]
  },
  {
    "id": "employment_003",
    "service": "Employment Exchange",
    "category": "Process",
    "question": "What are the steps involved in the Employment Exchange Registration?",
    "answer": "The Employment Exchange Registration is divided into 6 main steps shown in a progress tracker: (1) Personal – basic personal information, (2) Address – present and permanent address, (3) Qualification – educational qualifications, (4) Language – languages known, (5) Others – physical, caste, willingness, and other details, and (6) Uploads – required documents.",
    "keywords": [
      "steps",
      "employment exchange",
      "registration process",
      "6 steps",
      "progress"
    ]
  },
  {
    "id": "employment_004",
    "service": "Employment Exchange",
    "category": "Qualification",
    "question": "How do I add my educational qualification in the Employment Exchange Registration?",
    "answer": "In Step 3 (Qualification), click 'Add Qualification' to open a popup form. Fill in: Exam Passed (e.g., 8th, 10th, 12th, Graduation), Board/University, Subjects (click + to add multiple), Division/Grade, Year of Passing (digits only), Course Duration (years), School/Institute Name, Medium (e.g., English, Manipuri), and Percentage/CGPA. Click 'Add' to save. You can add multiple qualifications.",
    "keywords": [
      "qualification",
      "add qualification",
      "education",
      "exam",
      "board",
      "employment exchange"
    ]
  },
  {
    "id": "employment_005",
    "service": "Employment Exchange",
    "category": "Experience",
    "question": "How do I add work experience in the Employment Exchange Registration?",
    "answer": "In Step 4 (Experience), select 'Yes' for 'Do you have Experience?' Then click 'Add Experience' to open a popup form. Fill in: Name of Employer/Company, Pay on Leaving (per month), From Date, To Date, Nature of Work, Experience Type (Full-time/Part-time/Contract/Internship), Type of Job, Post Held, and Reason for Leaving. Click 'Add' to save. You can add multiple experiences.",
    "keywords": [
      "experience",
      "work experience",
      "add experience",
      "employer",
      "employment exchange"
    ]
  },
  {
    "id": "employment_006",
    "service": "Employment Exchange",
    "category": "Experience",
    "question": "What types of experience can I add in the Employment Exchange Registration?",
    "answer": "You can add various types of experience: Experience Type options include Full-time, Part-time, Contract, and Internship. Type of Job options include Administration, Technical, Skilled, Unskilled, and Office Assistance.",
    "keywords": [
      "experience type",
      "full-time",
      "part-time",
      "contract",
      "internship",
      "employment exchange"
    ]
  },
  {
    "id": "employment_007",
    "service": "Employment Exchange",
    "category": "Language",
    "question": "How do I add languages in the Employment Exchange Registration?",
    "answer": "In Step 5 (Language), click 'Add Language' to add a language entry. The language table has columns for: Serial No., Language Known, Read (Yes/No), Speak (Yes/No), Write (Yes/No), and Action (Edit/Delete). You can specify your proficiency in reading, speaking, and writing for each language added.",
    "keywords": [
      "language",
      "add language",
      "read",
      "speak",
      "write",
      "employment exchange"
    ]
  },
  {
    "id": "employment_008",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What information is collected in the 'Others' step of Employment Exchange Registration?",
    "answer": "Step 6 (Others) collects four categories of information: (1) Physical Standard – height, weight, chest, glasses, sports, NCC level, disability, ex-serviceman status, blood group; (2) Caste Details – main caste, sub caste, certificate info; (3) Willingness Details – employment sector, vacancy, training willingness; and (4) Other Details – preferred work location, employment status, residence proof, expected salary, and state/central priorities.",
    "keywords": [
      "others",
      "physical standard",
      "caste details",
      "willingness",
      "employment exchange",
      "step 6"
    ]
  },
  {
    "id": "employment_009",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What physical details are required in the Employment Exchange Registration?",
    "answer": "The Physical Standard section requires: Wear Glasses (Yes/No), Height (in cm), Weight (in kg), Chest (in cm), Main Sport (dropdown), Sports Level (dropdown), Sports Grade (dropdown), NCC Level (dropdown), Disability more than 40% (Yes/No), Disability Type (if applicable), Whether Ex-serviceman (Yes/No), and Blood Group (dropdown).",
    "keywords": [
      "physical standard",
      "height",
      "weight",
      "disability",
      "blood group",
      "employment exchange"
    ]
  },
  {
    "id": "employment_010",
    "service": "Employment Exchange",
    "category": "Uploads",
    "question": "What documents are required to be uploaded for Employment Exchange Registration?",
    "answer": "Required uploads include: (1) Passport Photo (plain background, under 100 KB), (2) Aadhaar Card front image (under 100 KB), (3) Aadhaar Card back image (under 100 KB), (4) Qualification Certificates, (5) Experience Certificates (if applicable), (6) Proof of Residence, (7) Domicile Certificate, (8) Caste Certificate, (9) Date of Birth Certificate, and (10) Other Documents as required.",
    "keywords": [
      "documents",
      "uploads",
      "required documents",
      "aadhaar",
      "passport photo",
      "employment exchange"
    ]
  },
  {
    "id": "employment_011",
    "service": "Employment Exchange",
    "category": "Uploads",
    "question": "What is the maximum file size for uploads in Employment Exchange Registration?",
    "answer": "The maximum file size for uploads is 100 KB per file. This applies to passport photos, Aadhaar card images (front and back), and other supporting documents. Make sure all your files are compressed to under 100 KB before uploading.",
    "keywords": [
      "file size",
      "upload limit",
      "100 KB",
      "photo size",
      "document size",
      "employment exchange"
    ]
  },
  {
    "id": "employment_012",
    "service": "Employment Exchange",
    "category": "Uploads",
    "question": "What are the requirements for the passport photo upload?",
    "answer": "The passport photo must have a plain background and the file size must be under 100 KB. Make sure the photo clearly shows your face and meets standard passport photo requirements.",
    "keywords": [
      "passport photo",
      "photo requirements",
      "plain background",
      "upload",
      "employment exchange"
    ]
  },
  {
    "id": "employment_013",
    "service": "Employment Exchange",
    "category": "Uploads",
    "question": "How do I select a processing office for my Employment Exchange Registration?",
    "answer": "In the Uploads step (Step 6), there is a 'Processing Office Selection' section where you need to select your District (e.g., Imphal West) and then choose your Processing Office from a dropdown list.",
    "keywords": [
      "processing office",
      "district",
      "office selection",
      "employment exchange",
      "uploads"
    ]
  },
  {
    "id": "employment_014",
    "service": "Employment Exchange",
    "category": "Submission",
    "question": "What is the declaration I need to agree to before submitting my Employment Exchange Registration?",
    "answer": "Before submitting, you must read and check the declaration checkbox that states: 'I agree and Continue'. The declaration warns that if any information furnished by the applicant turns out to be false, the registration is liable to be cancelled. This checkbox is mandatory for submission.",
    "keywords": [
      "declaration",
      "agree",
      "I agree",
      "terms",
      "submission",
      "false information",
      "employment exchange"
    ]
  },
  {
    "id": "employment_015",
    "service": "Employment Exchange",
    "category": "Submission",
    "question": "What are the two save/submit options available before final submission of Employment Exchange Registration?",
    "answer": "Before final submission, there are two buttons: (1) 'Save All' – saves your progress without final submission, allowing you to return later to complete the application; and (2) 'Submit Application' – finalizes and submits your application for processing.",
    "keywords": [
      "save all",
      "submit application",
      "save draft",
      "submit",
      "employment exchange"
    ]
  },
  {
    "id": "employment_016",
    "service": "Employment Exchange",
    "category": "Submission",
    "question": "What happens after I successfully submit my Employment Exchange Registration?",
    "answer": "After successful submission, a popup appears showing: (1) A success message 'Application Submitted Successfully', (2) Your Application Number (e.g., 16/20260218002), and (3) A reminder to keep this number for future reference and for tracking. You can click 'Download' to save your acknowledgement receipt or 'Okay' to close the popup.",
    "keywords": [
      "after submission",
      "application submitted",
      "application number",
      "acknowledgement",
      "employment exchange"
    ]
  },
  {
    "id": "employment_017",
    "service": "Employment Exchange",
    "category": "Submission",
    "question": "How do I download my Employment Exchange application receipt?",
    "answer": "After successful submission, a popup appears with a 'Download' button that lets you download your acknowledgement receipt. You can also download it later by going to Sidebar → Applications → Applied List, finding your application, and clicking the download (⬇) icon.",
    "keywords": [
      "download receipt",
      "acknowledgement",
      "receipt",
      "application number",
      "employment exchange"
    ]
  },
  {
    "id": "employment_018",
    "service": "Employment Exchange",
    "category": "Tracking",
    "question": "How do I track my Employment Exchange Registration application?",
    "answer": "To track your application: Go to Sidebar → Applications → Applied List. You will see a table with your Application No, Applicant Name, Date of Submission, and Status. Click the View (👁) icon to see a detailed Application Status Timeline, which shows each stage (e.g., Submitted) with date, time, and status message.",
    "keywords": [
      "track application",
      "application status",
      "applied list",
      "tracking",
      "employment exchange"
    ]
  },
  {
    "id": "employment_019",
    "service": "Employment Exchange",
    "category": "Tracking",
    "question": "What does 'Submitted' status mean in the Applied List?",
    "answer": "A 'Submitted' status means your Employment Exchange Registration application has been successfully submitted and an acknowledgement receipt has been generated. Your application is now waiting for government officials to review and process it.",
    "keywords": [
      "submitted status",
      "application status",
      "applied list",
      "acknowledgement",
      "employment exchange"
    ]
  },
  {
    "id": "employment_020",
    "service": "Employment Exchange",
    "category": "Tracking",
    "question": "How do I search for my application in the Applied List?",
    "answer": "In the Applied List (Sidebar → Applications → Applied List), there is a search bar where you can search for your application by entering your Application Number.",
    "keywords": [
      "search application",
      "applied list",
      "application number",
      "find application",
      "employment exchange"
    ]
  },
  {
    "id": "employment_021",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What willingness details are required in the Employment Exchange Registration?",
    "answer": "The Willingness Details section requires: Employment Sector Willingness, Vacancy Willingness, Other Willingness, Whether Willing to Undergo Training (Yes/No), Whether Willing to Specify Trade(s) (Yes/No), and Non-Availability period (From Date and To Date – for dates when you are not available).",
    "keywords": [
      "willingness",
      "employment sector",
      "training",
      "non-availability",
      "employment exchange"
    ]
  },
  {
    "id": "employment_022",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What salary details do I need to provide in the Employment Exchange Registration?",
    "answer": "In the 'Other Details' section of Step 6, you need to provide: Expected Minimum Salary for Outside Job (Rs per month) and Expected Minimum Salary for Local Job (Rs per month).",
    "keywords": [
      "salary",
      "expected salary",
      "minimum salary",
      "outside job",
      "local job",
      "employment exchange"
    ]
  },
  {
    "id": "employment_023",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What is the caste certificate information required in Employment Exchange Registration?",
    "answer": "The Caste Details section requires: Main Caste (dropdown), Sub Caste (dropdown), Center Name, Certificate No. (enter N/A if not available), Certificate Issued Date, Certificate Issued By Whom (enter N/A if not available), and Remark.",
    "keywords": [
      "caste certificate",
      "caste details",
      "sub caste",
      "certificate number",
      "employment exchange"
    ]
  },
  {
    "id": "employment_024",
    "service": "Employment Exchange",
    "category": "Rules",
    "question": "What are the important rules to remember when filling the Employment Exchange Registration?",
    "answer": "Key rules: (1) Fields marked with * are mandatory, (2) Passport photo and Aadhaar images must be under 100 KB, (3) Enter 'N/A' where certificate details are not available (as instructed), (4) You must tick 'I agree and Continue' before submitting, (5) False information can lead to cancellation of registration, (6) Always save or download your acknowledgement receipt after submission.",
    "keywords": [
      "rules",
      "mandatory fields",
      "file size",
      "N/A",
      "important tips",
      "employment exchange"
    ]
  },
  {
    "id": "employment_025",
    "service": "Employment Exchange",
    "category": "Rules",
    "question": "What happens if I provide wrong information in my Employment Exchange Registration?",
    "answer": "The declaration on the application form states that if any information furnished by the applicant turns out to be false, your registration is liable to be cancelled. Therefore, ensure all details entered are accurate and truthful.",
    "keywords": [
      "false information",
      "wrong information",
      "cancellation",
      "registration cancelled",
      "employment exchange"
    ]
  },
  {
    "id": "employment_026",
    "service": "Employment Exchange",
    "category": "Others",
    "question": "What is the 'State Priority' in the Employment Exchange Registration Other Details section?",
    "answer": "The 'State Priority' is a dropdown field in the Other Details section where you can select your priority for state government employment. If you set State Priority or Priority for Central to 'Yes', you must additionally provide: Certificate No., Certifying Authority, Period of Work(s), and Certificate Date.",
    "keywords": [
      "state priority",
      "central priority",
      "employment exchange",
      "priority",
      "certificate"
    ]
  },

  {
    "id": "general_000",
    "service": "General",
    "category": "Overview",
    "question": "what info can i get from settings menu?",
    "answer": "The settings menu in e-Seba Manipur allows you to manage your account preferences, update your profile information, change your password, and view account-related details.",
    "keywords": [
      "change password",
      "password",
      "account",
      "security",
      "update password"
    ]
  },

  {
    "id": "general_001",
    "service": "General",
    "category": "Account",
    "question": "How do I change my password on e-Seba Manipur?",
    "answer": "To change your password, log in to your account and go to the sidebar menu. Under the 'Account' section, click 'Change Password'. Enter your current and new password to update it.",
    "keywords": [
      "change password",
      "password",
      "account",
      "security",
      "update password"
    ]
  },
  {
    "id": "general_002",
    "service": "General",
    "category": "Account",
    "question": "How do I edit my profile on e-Seba Manipur?",
    "answer": "To edit your profile, log in and go to the sidebar menu. Under the 'Account' section, click 'Edit Profile' to update your personal information.",
    "keywords": [
      "edit profile",
      "update profile",
      "account",
      "personal information"
    ]
  },
  {
    "id": "general_003",
    "service": "General",
    "category": "Account",
    "question": "How do I log out of e-Seba Manipur?",
    "answer": "To log out, click 'Logout' at the bottom of the sidebar menu in your dashboard. This will end your current session.",
    "keywords": [
      "logout",
      "sign out",
      "end session",
      "account"
    ]
  },
  {
    "id": "general_004",
    "service": "General",
    "category": "Dashboard",
    "question": "What is a 'Saved Draft' on the dashboard?",
    "answer": "A 'Saved Draft' is an incomplete application that you have saved but not yet submitted. You can resume these applications later. The number of saved drafts is displayed as a KPI card on the dashboard.",
    "keywords": [
      "saved draft",
      "draft",
      "incomplete application",
      "resume application",
      "dashboard"
    ]
  },
  {
    "id": "general_005",
    "service": "General",
    "category": "Registration",
    "question": "Is Aadhaar number mandatory for registration on e-Seba Manipur?",
    "answer": "Yes, the Aadhaar Number (12-digit unique identity number) is mandatory for registration on e-Seba Manipur. You also need to provide your Name as per Aadhaar, which must match your Aadhaar card exactly.",
    "keywords": [
      "aadhaar",
      "mandatory",
      "aadhaar number",
      "registration",
      "required"
    ]
  },
  {
    "id": "general_006",
    "service": "General",
    "category": "Contact",
    "question": "How can I contact support for e-Seba Manipur?",
    "answer": "You can contact e-Seba Manipur support by clicking 'CONTACT US' in the top navigation bar of the landing page. This will provide you with contact information for support.",
    "keywords": [
      "contact",
      "support",
      "help",
      "contact us",
      "helpline"
    ]
  },
  {
    "id": "general_007",
    "service": "General",
    "category": "Dashboard",
    "question": "What does the 'Issued List' in my dashboard show?",
    "answer": "The 'Issued List' under Applications in your dashboard shows all applications that have been successfully approved and for which certificates have been generated. You can download these certificates from the Issued List.",
    "keywords": [
      "issued list",
      "approved",
      "certificate generated",
      "completed applications",
      "dashboard"
    ]
  },
  {
    "id": "general_008",
    "service": "General",
    "category": "Dashboard",
    "question": "What does the 'Rejected List' in my dashboard show?",
    "answer": "The 'Rejected List' under Applications in your dashboard shows all applications that were denied or rejected by the government department. You may need to re-apply or resolve the issues mentioned in the rejection.",
    "keywords": [
      "rejected list",
      "rejected application",
      "denied",
      "application rejected",
      "dashboard"
    ]
  },
  {
    "id": "general_009",
    "service": "General",
    "category": "Dashboard",
    "question": "What is the Status Distribution chart on the dashboard?",
    "answer": "The Status Distribution is a visual donut chart on the dashboard that provides a graphical representation of all your application statuses — showing the proportion of Submitted, In Progress, Issued, and Rejected applications at a glance.",
    "keywords": [
      "status distribution",
      "donut chart",
      "chart",
      "visual",
      "application overview",
      "dashboard"
    ]
  },
  {
    "id": "general_010",
    "service": "General",
    "category": "Dashboard",
    "question": "What is the 'Recent Activity' section on the dashboard?",
    "answer": "The 'Recent Activity' section on the dashboard is a timeline log that shows your latest actions and application events. It helps you quickly see what you have recently done on the portal.",
    "keywords": [
      "recent activity",
      "timeline",
      "activity log",
      "dashboard",
      "latest actions"
    ]
  }
]
# ─── In-memory session storage ───────────────────────────────────────────────
sessions: dict = {}

# ─── Helper functions ─────────────────────────────────────────────────────────

def get_services():
    services = list(set(item["service"] for item in KNOWLEDGE_BASE))
    return sorted(services)

def get_categories_for_service(service: str):
    cats = list(set(item["category"] for item in KNOWLEDGE_BASE if item["service"] == service))
    return sorted(cats)

def get_questions_for_category(service: str, category: str):
    return [
        {"id": item["id"], "question": item["question"]}
        for item in KNOWLEDGE_BASE
        if item["service"] == service and item["category"] == category
    ]

def get_answer(question_id: str):
    for item in KNOWLEDGE_BASE:
        if item["id"] == question_id:
            return item
    return None

def get_service_overview(service: str):
    """Return the overview answer for a service (entry whose id ends with '000')."""
    for item in KNOWLEDGE_BASE:
        if item["service"] == service and item["id"].endswith("000"):
            return item["answer"]
    return None

# ─── Pydantic Models ──────────────────────────────────────────────────────────

class UserInfo(BaseModel):
    name: str
    phone: str

class SessionCreate(BaseModel):
    user_info: UserInfo

class ChatRequest(BaseModel):
    session_id: str
    action: str          # "select_service" | "select_category" | "select_question" | "back"
    value: Optional[str] = None

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/api/session/start")
def start_session(data: SessionCreate):
    """Register user and create a chat session."""
    # Validate phone
    phone = data.user_info.phone.strip()
    if not re.match(r"^[6-9]\d{9}$", phone):
        raise HTTPException(status_code=422, detail="Please enter a valid 10-digit Indian mobile number.")
    
    name = data.user_info.name.strip()
    if len(name) < 2:
        raise HTTPException(status_code=422, detail="Please enter your full name.")

    import uuid
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "user": {"name": name, "phone": phone},
        "created_at": datetime.now().isoformat(),
        "history": [],
        "state": "service_selection",
        "current_service": None,
        "current_category": None,
    }

    return {
        "session_id": session_id,
        "message": f"Welcome, {name}! 🙏 How can I help you today?",
        "state": "service_selection",
        "services": get_services(),
    }

@app.post("/api/chat")
def chat(req: ChatRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please start a new session.")

    session = sessions[req.session_id]
    user_name = session["user"]["name"]
    action = req.action
    value = req.value

    # ── Handle BACK ──────────────────────────────────────────────────────────
    if action == "back":
        if session["state"] == "question_selection":
            session["state"] = "category_selection"
            session["current_category"] = None
            cats = get_categories_for_service(session["current_service"])
            overview = get_service_overview(session["current_service"])
            msg = f"What topic would you like help with under **{session['current_service']}**?"
            if overview:
                msg += f"\n\n📋 **Overview:** {overview}"
            return {
                "state": "category_selection",
                "message": msg,
                "categories": cats,
                "service": session["current_service"],
            }
        elif session["state"] == "category_selection":
            session["state"] = "service_selection"
            session["current_service"] = None
            return {
                "state": "service_selection",
                "message": "Please select a service to continue.",
                "services": get_services(),
            }
        elif session["state"] == "answer":
            session["state"] = "question_selection"
            qs = get_questions_for_category(session["current_service"], session["current_category"])
            return {
                "state": "question_selection",
                "message": f"Here are questions under **{session['current_category']}**. Please select one:",
                "questions": qs,
                "service": session["current_service"],
                "category": session["current_category"],
            }
        else:
            return {
                "state": "service_selection",
                "message": "Please select a service to continue.",
                "services": get_services(),
            }

    # ── Select Service ────────────────────────────────────────────────────────
    if action == "select_service":
        if value not in get_services():
            raise HTTPException(status_code=400, detail="Invalid service selected.")
        session["current_service"] = value
        session["current_category"] = None
        session["state"] = "category_selection"
        cats = get_categories_for_service(value)
        overview = get_service_overview(value)
        msg = f"You selected **{value}**. What topic would you like help with?"
        if overview:
            msg += f"\n\n📋 **Overview:** {overview}"
        return {
            "state": "category_selection",
            "message": msg,
            "categories": cats,
            "service": value,
        }

    # ── Select Category ───────────────────────────────────────────────────────
    if action == "select_category":
        if not session["current_service"]:
            raise HTTPException(status_code=400, detail="No service selected.")
        valid_cats = get_categories_for_service(session["current_service"])
        if value not in valid_cats:
            raise HTTPException(status_code=400, detail="Invalid category.")
        session["current_category"] = value
        session["state"] = "question_selection"
        qs = get_questions_for_category(session["current_service"], value)
        return {
            "state": "question_selection",
            "message": f"Here are questions under **{value}**. Please select one:",
            "questions": qs,
            "service": session["current_service"],
            "category": value,
        }

    # ── Select Question ───────────────────────────────────────────────────────
    if action == "select_question":
        item = get_answer(value)
        if not item:
            raise HTTPException(status_code=404, detail="Question not found.")
        session["state"] = "answer"
        session["history"].append({
            "question_id": value,
            "question": item["question"],
            "timestamp": datetime.now().isoformat(),
        })
        return {
            "state": "answer",
            "message": item["answer"],
            "question": item["question"],
            "service": item["service"],
            "category": item["category"],
        }

    raise HTTPException(status_code=400, detail="Unknown action.")

@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    s = sessions[session_id]
    return {
        "user": s["user"],
        "state": s["state"],
        "current_service": s["current_service"],
        "current_category": s["current_category"],
        "history": s["history"],
    }

@app.get("/api/services")
def list_services():
    services = get_services()
    result = []
    for svc in services:
        cats = get_categories_for_service(svc)
        count = sum(1 for item in KNOWLEDGE_BASE if item["service"] == svc)
        result.append({"service": svc, "categories": cats, "question_count": count})
    return result

@app.get("/health")
def health():
    return {"status": "ok", "service": "e-Seba Manipur Chatbot API"}

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")