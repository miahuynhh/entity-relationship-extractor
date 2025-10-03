/**
 * Main JavaScript application for Entity Relationship Visualizer
 * Handles user interactions and API communication
 */

// Global application state
const AppState = {
    isLoading: false,
    currentData: null,
    error: null
};

// DOM element references
const elements = {
    textInput: null,
    analyzeBtn: null,
    clearBtn: null,
    resultsSummary: null,
    relationshipCount: null,
    processingTime: null,
    loadingContainer: null,
    errorContainer: null,
    emptyState: null,
    graphContainer: null,
    errorText: null,
    btnText: null,
    btnLoading: null
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Entity Relationship Visualizer initialized');
    initializeElements();
    setupEventListeners();
    showEmptyState();
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    elements.textInput = document.getElementById('textInput');
    elements.analyzeBtn = document.getElementById('analyzeBtn');
    elements.clearBtn = document.getElementById('clearBtn');
    elements.resultsSummary = document.getElementById('resultsSummary');
    elements.relationshipCount = document.getElementById('relationshipCount');
    elements.processingTime = document.getElementById('processingTime');
    elements.loadingContainer = document.getElementById('loadingContainer');
    elements.errorContainer = document.getElementById('errorContainer');
    elements.emptyState = document.getElementById('emptyState');
    elements.graphContainer = document.getElementById('graphContainer');
    elements.errorText = document.getElementById('errorText');
    elements.btnText = elements.analyzeBtn.querySelector('.btn-text');
    elements.btnLoading = elements.analyzeBtn.querySelector('.btn-loading');
    
    console.log('DOM elements initialized');
}

/**
 * Setup event listeners for user interactions
 */
function setupEventListeners() {
    // Analyze button click
    elements.analyzeBtn.addEventListener('click', handleAnalyzeClick);
    
    // Clear button click
    elements.clearBtn.addEventListener('click', handleClearClick);
    
    // Enter key in textarea (Ctrl+Enter to analyze)
    elements.textInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            handleAnalyzeClick();
        }
    });
    
    // Reset view button (will be implemented in graph.js)
    const resetViewBtn = document.getElementById('resetViewBtn');
    if (resetViewBtn) {
        resetViewBtn.addEventListener('click', function() {
            if (window.resetGraphView) {
                window.resetGraphView();
            }
        });
    }
    
    console.log('Event listeners setup complete');
}

/**
 * Handle analyze button click
 */
async function handleAnalyzeClick() {
    const text = getTextFromInput();
    
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    if (text.length > 10000) {
        showError('Text is too long. Please enter text with 10,000 characters or less.');
        return;
    }
    
    try {
        setLoadingState(true);
        hideError();
        hideEmptyState();
        
        console.log('Starting text analysis...');
        const startTime = performance.now();
        
        const data = await analyzeText(text);
        
        const endTime = performance.now();
        const processingTime = Math.round(endTime - startTime);
        
        console.log('Analysis complete:', data);
        
        // Update UI with results
        updateResultsSummary(data, processingTime);
        showGraphContainer();
        
        // Initialize graph visualization (will be implemented in graph.js)
        if (window.initializeGraph && data.relationships) {
            window.initializeGraph(data.relationships);
        }
        
        AppState.currentData = data;
        
    } catch (error) {
        console.error('Analysis failed:', error);
        showError(error.message || 'Analysis failed. Please try again.');
        showEmptyState();
    } finally {
        setLoadingState(false);
    }
}

/**
 * Handle clear button click
 */
function handleClearClick() {
    console.log('Clearing application state');
    
    // Clear text input
    elements.textInput.value = '';
    
    // Reset application state
    AppState.isLoading = false;
    AppState.currentData = null;
    AppState.error = null;
    
    // Reset UI
    hideError();
    hideResultsSummary();
    hideGraphContainer();
    showEmptyState();
    
    // Clear graph if it exists
    if (window.clearGraph) {
        window.clearGraph();
    }
    
    // Focus on text input
    elements.textInput.focus();
}

/**
 * Get text from input field
 */
function getTextFromInput() {
    return elements.textInput.value.trim();
}

/**
 * Make API call to analyze text
 */
async function analyzeText(text) {
    const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
        throw new Error(data.error || 'Analysis failed');
    }
    
    return data;
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    AppState.isLoading = isLoading;
    
    if (isLoading) {
        elements.analyzeBtn.disabled = true;
        elements.btnText.style.display = 'none';
        elements.btnLoading.style.display = 'inline';
        elements.loadingContainer.style.display = 'flex';
    } else {
        elements.analyzeBtn.disabled = false;
        elements.btnText.style.display = 'inline';
        elements.btnLoading.style.display = 'none';
        elements.loadingContainer.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    AppState.error = message;
    elements.errorText.textContent = message;
    elements.errorContainer.style.display = 'flex';
    console.error('Error:', message);
}

/**
 * Hide error message
 */
function hideError() {
    AppState.error = null;
    elements.errorContainer.style.display = 'none';
}

/**
 * Show empty state
 */
function showEmptyState() {
    elements.emptyState.style.display = 'flex';
}

/**
 * Hide empty state
 */
function hideEmptyState() {
    elements.emptyState.style.display = 'none';
}

/**
 * Show graph container
 */
function showGraphContainer() {
    elements.graphContainer.style.display = 'block';
}

/**
 * Hide graph container
 */
function hideGraphContainer() {
    elements.graphContainer.style.display = 'none';
}

/**
 * Show results summary
 */
function showResultsSummary() {
    elements.resultsSummary.style.display = 'block';
}

/**
 * Hide results summary
 */
function hideResultsSummary() {
    elements.resultsSummary.style.display = 'none';
}

/**
 * Update results summary with analysis data
 */
function updateResultsSummary(data, processingTime) {
    elements.relationshipCount.textContent = data.count || 0;
    elements.processingTime.textContent = `${processingTime}ms`;
    showResultsSummary();
}

/**
 * Utility function to log application state
 */
function logAppState() {
    console.log('App State:', AppState);
    console.log('Current Data:', AppState.currentData);
}

// Make utility functions available globally for debugging
window.AppState = AppState;
window.logAppState = logAppState;
