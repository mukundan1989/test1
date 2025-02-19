import streamlit as st
from custom_component.indexed_db_component import indexed_db_component

# Streamlit app
st.title("Streamlit IndexedDB Example")

# Display the custom component
indexed_db_component()

# Listen for messages from the JavaScript
st.write("Logs and Data from IndexedDB:")
log_placeholder = st.empty()
data_placeholder = st.empty()

# Handle messages from JavaScript
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'data' not in st.session_state:
    st.session_state.data = None

# JavaScript to Python communication
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'data' || event.data.type === 'log') {
        // Send the message to Streamlit
        window.parent.streamlitApi.sendMessage(event.data);
    }
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
