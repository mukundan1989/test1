# app.py
import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript to interact with IndexedDB
indexed_db_script = """
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
        window.parent.postMessage({type: 'data', data: data}, '*');
    };

    request.onerror = function(event) {
        console.log("Error retrieving data");
        window.parent.postMessage({type: 'log', message: 'Error retrieving data'}, '*');
    };
}

</script>
<button onclick="addData()">Add Data</button>
<button onclick="getData()">Get Data</button>
"""

# Streamlit app
st.title("Streamlit IndexedDB Example")

# Display the custom HTML component
components.html(indexed_db_script, height=100)

# Listen for messages from the JavaScript
st.write("Logs and Data from IndexedDB:")
log_placeholder = st.empty()
data_placeholder = st.empty()

# JavaScript to Python communication
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'data' || event.data.type === 'log') {
        window.parent.streamlitApi.sendMessage(event.data);
    }
});
</script>
""", height=0)

# Handle messages from JavaScript
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'data' not in st.session_state:
    st.session_state.data = None

def handle_message(message):
    if message['type'] == 'data':
        st.session_state.data = message['data']
    elif message['type'] == 'log':
        st.session_state.logs.append(message['message'])

# Register the message handler
components.html("""
<script>
window.parent.streamlitApi.registerMessageHandler(function(message) {
    handle_message(message);
});
</script>
""", height=0)

# Display logs and data
if st.session_state.logs:
    log_placeholder.write("Logs:")
    for log in st.session_state.logs:
        log_placeholder.write(log)

if st.session_state.data:
    data_placeholder.write("Retrieved Data:")
    data_placeholder.write(st.session_state.data)
