# EmailJS Setup Guide

This guide will help you set up EmailJS so your contact form can send emails directly to your inbox.

## Step 1: Create an EmailJS Account

1. Go to [https://www.emailjs.com/](https://www.emailjs.com/)
2. Click "Sign Up" and create a free account
3. Verify your email address

## Step 2: Add an Email Service

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/admin)
2. Click on **Email Services** in the left sidebar
3. Click **Add New Service**
4. Choose your email provider (Gmail, Outlook, etc.)
5. Follow the instructions to connect your email account
6. **Note your Service ID** (you'll need this later)

## Step 3: Create an Email Template

1. Go to **Email Templates** in the left sidebar
2. Click **Create New Template**
3. Use the following template:

   **Template Name:** Contact Form
   
   **Subject:** New Message from Portfolio Contact Form
   
   **Content:**
   ```
   You have a new message from your portfolio website.
   
   From: {{from_name}}
   Email: {{from_email}}
   
   Message:
   {{message}}
   ```
   
4. Click **Save**
5. **Note your Template ID** (you'll need this later)

## Step 4: Get Your Public Key

1. Go to **Account** → **General** in the left sidebar
2. Find your **Public Key** (also called API Key)
3. **Copy this key** (you'll need this later)

## Step 5: Update Your Code

Open `script.js` and replace the following placeholders:

1. **Line 104:** Replace `"YOUR_PUBLIC_KEY"` with your actual Public Key from Step 4
2. **Line 137:** Replace `'YOUR_SERVICE_ID'` with your Service ID from Step 2
3. **Line 138:** Replace `'YOUR_TEMPLATE_ID'` with your Template ID from Step 3

Example:
```javascript
emailjs.init("abc123xyz456"); // Your actual Public Key

await emailjs.send(
    'service_abc123',    // Your actual Service ID
    'template_xyz789',   // Your actual Template ID
    {
        from_name: name,
        from_email: email,
        message: message,
        to_email: 'yukktas@bu.edu'
    }
);
```

## Step 6: Test Your Form

1. Save all your files
2. Push to GitHub
3. Visit your live website
4. Fill out the contact form and submit
5. Check your email inbox for the message

## Free Tier Limits

EmailJS free tier includes:
- 200 emails per month
- All basic features
- Perfect for personal portfolios

## Troubleshooting

**Form not sending emails?**
- Check browser console for errors (F12 → Console)
- Verify all three IDs are correct (Public Key, Service ID, Template ID)
- Make sure your email service is connected in EmailJS dashboard
- Check that your template variables match: `{{from_name}}`, `{{from_email}}`, `{{message}}`

**Getting errors?**
- Make sure EmailJS script is loaded (check Network tab in browser)
- Verify your Public Key is correct
- Check that your Service ID and Template ID match what's in your EmailJS dashboard

## Need Help?

- EmailJS Documentation: [https://www.emailjs.com/docs/](https://www.emailjs.com/docs/)
- EmailJS Support: [https://www.emailjs.com/support/](https://www.emailjs.com/support/)

