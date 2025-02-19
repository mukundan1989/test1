import streamlit.components.v1 as components

# Create a custom component
def indexed_db_component():
    # HTML and JavaScript to interact with IndexedDB
    html_code = """
    <script>
    // Open (or create) the database
    var request = indexedDB.open("MyTestDB", 1);

    request.onupgradeneeded = function(event) {
        var db = event.target.result;
        var objectStore = db.createObjectStore("myStore", { keyPath: "id" });
    };

    request.onsuccess = function(event) {
        var db = event.target.result;
        window.db = db;
    };

    function addData() {
        var transaction = window.db.transaction(["myStore"], "readwrite");
        var store = transaction.objectStore("myStore");
        var request = store.add({ id: 1, name: "John Doe", age: 30 });

        request.onsuccess = function(event) {
            console.log("Data added successfully");
            // Send a message to Streamlit
            window.parent.postMessage({type: 'log', message: 'Data added successfully'}, '*');
        };

        request.onerror = function(event) {
            console.log("Error adding data");
            window.parent.postMessage({type: 'log', message: 'Error adding data'}, '*');
        };
    }

    function getData() {
        var transaction = window.db.transaction(["myStore"], "readonly");
        var store = transaction.objectStore("myStore");
        var request = store.get(1);

        request.onsuccess = function(event) {
            var data = event.target.result;
            console.log("Retrieved data:", data);
            // Send a message to Streamlit
            window.parent.postMessage({type: 'data', data: data}, '*');
        };

        request.onerror = function(event) {
            console.log("Error retrieving data");
            window.parent.postMessage({type: 'log', message: 'Error retrieving data'}, '*');
        };
    }

    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'addData') {
            addData();
        } else if (event.data.type === 'getData') {
            getData();
        }
    });
    </script>
    <button onclick="addData()">Add Data</button>
    <button onclick="getData()">Get Data</button>
    """

    # Render the custom component
    components.html(html_code, height=100)
