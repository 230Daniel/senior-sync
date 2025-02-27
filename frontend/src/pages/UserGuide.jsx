const UserGuide = () => {
    return (
        <div>
            <div>
                <h1>Support</h1>
            </div>

            <h2>Welcome to the support page</h2>

            <h3>Below are three sections that will help you navigate and use Senior Sync</h3>

            <h3>If you require any further support please do not hesitate to contact us via the button at the bottom.</h3>

            <div style={{ marginTop: '20px' }}>
                <h2>Section 1: Overview</h2>
                <p>
                    This software is for the purpose of monitoring a patient's health through wearable sensors. 
                    These sensors transmit their data to the Senior Sync app which records and displays data in real time to provide insights into a patient's condition.
                    When a metric is recorded outside a healthy range, alerts will be sent to patients' set emergency contacts so further action can be taken.
                </p>
            </div>

            <div style={{ marginTop: '20px' }}>
                <h2>Section 2: Getting Started</h2>
                <p>
                    This section helps you get started with the basics of using Senior Sync.<br /><br />
                    Navigation through Senior Sync is achieved through the bar at the top. This bar contains four icons which can be used to access the different sections of the dashboard.<br /><br />
                    To access the home page containing the metrics: click on the Senior Sync icon on the left-hand side.<br /><br />
                    To access the alerts page: click on the exclamation icon.<br /><br />
                    To access Support: click on the question icon.<br /><br />
                    Senior Sync also comes with a theme selector which can be used to change the color scale of the page to make it more accessible. This can be used through the icon between the alerts and support page.
                </p>
            </div>

            <div style={{ marginTop: '20px' }}>
                <h2>Section 3: FAQs</h2>
                <p>
                    Frequently asked questions:<br /><br />
                    How do I connect my wearable sensors to the dashboard? To connect your wearable sensors, ensure they are powered on and within range. Open the Senior Sync app, navigate to the 'Devices' section, and follow the on-screen instructions to pair your sensors with the dashboard.<br /><br />
                    What types of health data can I monitor with this dashboard? The dashboard allows you to monitor various health metrics, including heart rate, blood pressure, oxygen levels, sleep patterns, and physical activity. The data is displayed in real-time to provide comprehensive insights into your health.<br /><br />
                    Can I customize the dashboard to show the data I need? You can customize the dashboard by selecting the 'Settings' icon. From there, you can choose which health metrics to display, set thresholds for alerts, and arrange the layout to suit your preferences.<br /><br />
                    Is my health data secure on this platform? Yes, your health data is secure. The platform uses advanced encryption methods to protect your data. Additionally, access to your data is restricted to authorized users only, ensuring your privacy is maintained.<br /><br />
                    Can I share my health data with my healthcare provider? Yes, you can share your health data with your healthcare provider. The dashboard includes a feature that allows you to generate reports and share them via email, ensuring your provider has access to the latest information.
                </p>
            </div>

            <div style={{ marginTop: '20px', marginBottom: '20px'}}>
                <button 
                    onClick={() => window.location.href='mailto:khadija.khan.267@cranfield.ac.uk?subject=Data%20inquiry.'} 
                    style={{ padding: '10px 20px', backgroundColor: '#ccc', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
                >
                    Contact Support
                </button>
            </div>
        </div>
    );
};

export default UserGuide;