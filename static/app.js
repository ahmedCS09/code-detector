// 1. Add an event listener to the form with ID 'reviewForm' for the 'submit' event
document.getElementById('reviewForm').addEventListener('submit', async function(e) {
  
  // 2. Prevent the default form submission behavior which would reload the page
  e.preventDefault();
  
  // 3. Get the value from the textarea/input field with ID 'code'
  const code = document.getElementById('code').value;

  // 4. Send a POST request to the server endpoint at 'http://127.0.0.1:5000/review'
  const response = await fetch('http://127.0.0.1:5000/review', {
    // 5. Specify this is a POST request
    method: 'POST',
    // 6. Set the request header to indicate we're sending JSON data
    headers: { 'Content-Type': 'application/json' },
    // 7. Convert the code data to JSON format and include it in the request body
    body: JSON.stringify({ code })
  });

  // 8. Wait for the response and parse it as JSON
  const data = await response.json();
  
  // 9. Get the HTML element with ID 'results' where we'll display the output
  const resultsEl = document.getElementById('results');
  
  // 10. Clear any existing content in the results element
  resultsEl.innerHTML = '';
  
  // 11. Loop through each message in the analysis array (or empty array if none exists)
  (data.analysis || []).forEach(msg => {
    // 12. Create a new list item element for each message
    const li = document.createElement('li');
    
    // 13. Set the text content of the list item to the analysis message
    li.textContent = msg;
    
    // 14. Add a CSS class to the list item for styling
    li.className = 'list-group-item';
    
    // 15. Add the list item to the results container
    resultsEl.appendChild(li);
  });
});