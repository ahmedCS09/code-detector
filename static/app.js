// 1. Add an event listener to the form with ID 'reviewForm' for the 'submit' event
document.getElementById('reviewForm').addEventListener('submit', async function(e) {
  
  // 2. Prevent the default form submission behavior which would reload the page
  e.preventDefault();
  
  // 3. Get the value from the textarea/input field with ID 'code'
  const code = document.getElementById('code').value;

  // 9. Get the HTML element with ID 'results' where we'll display the output
  const resultsEl = document.getElementById('results');
  resultsEl.innerHTML = '<li class="list-group-item">Analyzing...</li>';

  try {
    const response = await fetch('/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });

    if (!response.ok) {
        throw new Error('Server error: ' + response.statusText);
    }

    const data = await response.json();
    resultsEl.innerHTML = '';
    
    (data.analysis || []).forEach(msg => {
      const li = document.createElement('li');
      li.textContent = msg;
      li.className = 'list-group-item';
      resultsEl.appendChild(li);
    });
  } catch (error) {
    resultsEl.innerHTML = `<li class="list-group-item list-group-item-danger">Error: ${error.message}. Please check if the server is running.</li>`;
    console.error('Fetch error:', error);
  }
});