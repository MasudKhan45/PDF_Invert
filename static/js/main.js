// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const btnBrowse = document.getElementById('btnBrowse');
const btnReset = document.getElementById('btnReset');
const btnRetry = document.getElementById('btnRetry');
const uploadCard = document.getElementById('uploadCard');

// State Elements
const processingState = document.getElementById('processingState');
const successState = document.getElementById('successState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');

// Current file
let selectedFile = null;

// Initialize event listeners
function init() {
    // Click events
    btnBrowse.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Reset buttons
    btnReset.addEventListener('click', resetUpload);
    btnRetry.addEventListener('click', resetUpload);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Prevent default drag behavior on the whole page
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, preventDefaults, false);
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.type.includes('pdf')) {
        showError('Please select a valid PDF file');
        return;
    }
    
    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    if (file.size > maxSize) {
        showError('File size exceeds 50MB limit');
        return;
    }
    
    selectedFile = file;
    uploadPDF(file);
}

async function uploadPDF(file) {
    // Show processing state
    showState('processing');
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Upload and process
        const response = await fetch('/invert', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process PDF');
        }
        
        // Get the blob
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `inverted_${file.name}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Show success state
        showState('success');
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while processing your PDF');
    }
}

function showState(state) {
    // Hide all states
    uploadArea.style.display = 'none';
    processingState.style.display = 'none';
    successState.style.display = 'none';
    errorState.style.display = 'none';
    
    // Show requested state with animation
    const stateElement = document.getElementById(`${state}State`);
    if (stateElement) {
        stateElement.style.display = 'block';
        stateElement.style.animation = 'none';
        setTimeout(() => {
            stateElement.style.animation = 'scaleIn 0.5s ease';
        }, 10);
    }
}

function showError(message) {
    errorMessage.textContent = message;
    showState('error');
}

function resetUpload() {
    // Reset file input
    fileInput.value = '';
    selectedFile = null;
    
    // Show upload area
    uploadArea.style.display = 'block';
    processingState.style.display = 'none';
    successState.style.display = 'none';
    errorState.style.display = 'none';
    
    // Reset upload area animation
    uploadArea.style.animation = 'none';
    setTimeout(() => {
        uploadArea.style.animation = 'fadeIn 0.5s ease';
    }, 10);
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
