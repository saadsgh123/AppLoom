function changeButtonDesign() {
    const button = document.getElementById('generate-btn');
    const icon = document.getElementById('button-icon');
    const loadingBar = document.getElementById('loading-bar');
    const resultSection = document.getElementById('result-section');
    const generateSection = document.getElementById('generate-section');

    // Change the button's design and show loading bar
    button.classList.add('clicked');
    icon.src = "https://via.placeholder.com/20/FF4C4C/FFFFFF?text=✓";
    loadingBar.style.display = "block";

    // Simulate an AJAX request to Flask to check if the result is ready
    fetch('/check_result')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Hide the loading bar and show result section
                loadingBar.style.display = "none";
                resultSection.style.display = "block";

                // Update the result section with the generated application info
                resultSection.innerHTML = `
                    <h2>Application Generated Successfully</h2>
                    <p>Your job application has been generated!</p>
                    <p>Job Title: ${document.getElementById('job-title').value}</p>
                    <p>Company: ${document.getElementById('company').value}</p>
                    <p>Description: ${document.getElementById('description').value}</p>
                    <p>Document Name: <a href="/path/to/generated/document/${data.document_name}" target="_blank">${data.document_name}</a></p>
                `;
            } else {
                // If the result is still pending
                resultSection.innerHTML = `
                    <h2>Generating Application...</h2>
                    <p>Please wait while we generate your application.</p>
                `;
            }
        })
        .catch(error => {
            // Handle any errors that may occur
            loadingBar.style.display = "none";
            resultSection.innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

function add_job_app(jobapp_id) {
    const obj_saved = document.getElementById('saved-response');
    const job_title = document.getElementById('job_title').value;
    const email = document.getElementById('email').value;
    const company = document.getElementById('company').value;
    const description = document.getElementById('description').value;  // Corrected field

    fetch('/submit',  // Corrected URL
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Specify JSON data
            },
            body: JSON.stringify({ job_title: job_title, email: email, company: company, description: description }),
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === "success") {
                obj_saved.style.display = "block";
                setTimeout(() => {
                    obj_saved.style.display = "none";
                }, 1000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
