import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# File paths for user and lead data
USERS_CSV = 'users.csv'
LEADS_CSV = 'leads.csv'

# Load user data from CSV
def load_users():
    try:
        return pd.read_csv(USERS_CSV)
    except FileNotFoundError:
        st.error("User data file not found.")
        return pd.DataFrame(columns=["username", "password", "name", "role"])

# Load lead data from CSV
def load_leads():
    try:
        return pd.read_csv(LEADS_CSV)
    except FileNotFoundError:
        st.error("Lead data file not found.")
        return pd.DataFrame(columns=["Lead ID", "Name", "Source", "Status", "Date", "Assigned To"])

# Save lead data to CSV
def save_leads(leads_df):
    leads_df.to_csv(LEADS_CSV, index=False)
    st.session_state.leads_df = leads_df  # Update the session state

# Initialize session state for user and leads
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# Load leads when session starts
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = load_leads()

# Updated role-based permissions
roles_permissions = {
    'Sales Team': ['View Leads', 'Update Status', 'Add Leads'],
    'Business Manager': ['View Leads', 'View Dashboard', 'Analyze Data']
}

def check_permission(permission):
    if st.session_state.current_user:
        return permission in roles_permissions.get(st.session_state.current_user['role'], [])
    return False

# Updated Lead Listing Screen
def lead_listing():
    st.title('Lead Listing')
    
    if check_permission('View Leads'):
        # Display current leads
        st.subheader("Current Leads")
        st.dataframe(st.session_state.leads_df)
    else:
        st.error("You are not authorized to view leads.")
    
    st.session_state.content_displayed = True

# Lead Management Screen (for adding leads)
def lead_management():
    st.title('Lead Management')
    
    if check_permission('Add Leads'):
        st.subheader('Add New Lead')
        with st.form(key='add_lead_form'):
            lead_name = st.text_input('Name')
            lead_source = st.selectbox('Source', ['Facebook', 'Google', 'Twitter', 'Website', 'Offline'])
            lead_status = st.selectbox('Status', ['New', 'Contacted', 'Not Interested', 'Qualified'])
            submit_btn = st.form_submit_button('Add Lead')

            if submit_btn:
                if lead_name and lead_source:
                    new_lead = pd.DataFrame([{
                        'Lead ID': len(st.session_state.leads_df) + 1,
                        'Name': lead_name,
                        'Source': lead_source,
                        'Status': lead_status,
                        'Date': datetime.now().strftime('%Y-%m-%d'),
                        'Assigned To': st.session_state.current_user['name']
                    }])
                    
                    # Add the new lead to the DataFrame using concat
                    st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_lead], ignore_index=True)
                    
                    # Save the updated DataFrame to CSV
                    save_leads(st.session_state.leads_df)
                    
                    st.success(f'Lead "{lead_name}" added successfully!')
                    
                    # Display confirmation of the new lead
                    st.subheader("New Lead Added")
                    st.dataframe(new_lead)
                else:
                    st.error('Please provide a lead name and select a source.')
    else:
        st.error("You are not authorized to add leads.")
    
    st.session_state.content_displayed = True

# Lead Details Screen
def lead_details():
    st.title('Lead Details')
    
    if check_permission('Update Status'):
        lead_id = st.number_input('Enter Lead ID', min_value=1, max_value=len(st.session_state.leads_df), step=1)
        lead = st.session_state.leads_df.loc[st.session_state.leads_df['Lead ID'] == lead_id]

        if not lead.empty:
            st.write(lead)

            st.subheader('Update Lead Status')
            new_status = st.selectbox('Update Status', ['New', 'Contacted', 'Not Interested', 'Qualified'])
            update_btn = st.button('Update Status')

            if update_btn:
                st.session_state.leads_df.loc[st.session_state.leads_df['Lead ID'] == lead_id, 'Status'] = new_status
                save_leads(st.session_state.leads_df)
                st.success('Lead status updated!')
        else:
            st.warning('Lead not found.')
    else:
        st.error("You are not authorized to update lead status.")
    
    st.session_state.content_displayed = True

# Dashboard Screen (Business Manager Role)
def dashboard():
    st.title('Business Manager Dashboard')
    
    if check_permission('View Dashboard'):
        st.subheader('Quick Overview of Leads')

        new_leads = st.session_state.leads_df[st.session_state.leads_df['Status'] == 'New']
        contacted_leads = st.session_state.leads_df[st.session_state.leads_df['Status'] == 'Contacted']
        qualified_leads = st.session_state.leads_df[st.session_state.leads_df['Status'] == 'Qualified']

        # Display lead counts in a box
        st.metric(label="New Leads:", value=len(new_leads))
        st.metric(label="Contacted Leads:", value=len(contacted_leads))
        st.metric(label="Qualified Leads:", value=len(qualified_leads))

        # Lead Status Distribution Bar Chart
        st.subheader('Lead Status Distribution')
        status_counts = st.session_state.leads_df['Status'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis', ax=ax)
        ax.set_xlabel('Lead Status')
        ax.set_ylabel('Count')
        ax.set_title('Number of Leads by Status')
        st.pyplot(fig)

        # Lead Sources Pie Charts
        st.subheader('Lead Sources Distribution')
        source_counts = st.session_state.leads_df['Source'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

        st.subheader('Lead Data Overview')
        st.dataframe(st.session_state.leads_df.head(5))
    else:
        st.error("You are not authorized to view the dashboard.")
    
    st.session_state.content_displayed = True
    
    

# Main function for role-based navigation
def main():
    st.sidebar.title(f"Welcome, {st.session_state.current_user['name']} ({st.session_state.current_user['role']})")

    # Use radio buttons for navigation
    nav_options = ["Lead Listing", "Lead Management", "Lead Details", "Dashboard"]
    nav_selection = st.sidebar.radio("Navigation", nav_options)

    if nav_selection == "Lead Listing":
        lead_listing()
    elif nav_selection == "Lead Management":
        lead_management()
    elif nav_selection == "Lead Details":
        lead_details()
    elif nav_selection == "Dashboard":
        dashboard()
    else:
        st.write("Welcome to the HSR Motors Lead Management System. Please select an option from the sidebar.")

    # Always show some content, even if no specific section is selected
    if not st.session_state.get('content_displayed', False):
        st.write("Select an option from the sidebar to view content.")

# Login function
def login():
    st.title('Login to HSR Motors Lead Management System')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        users_df = load_users()
        user_row = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        
        if not user_row.empty:
            st.session_state.logged_in = True
            st.session_state.current_user = {
                'name': user_row.iloc[0]['name'],
                'role': user_row.iloc[0]['role']
            }
            st.success(f"Logged in successfully as {st.session_state.current_user['name']}!")
            st.rerun()  # Rerun to load the main interface
        else:
            st.error('Invalid username or password')

# Main app logic
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()  # Show login screen if not logged in
    else:
        main()  # Show the main app interface after login