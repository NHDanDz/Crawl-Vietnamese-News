// Khởi tạo flatpickr và event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo flatpickr
    const dateRangePicker = flatpickr("#dateRange", {
        mode: "range",
        dateFormat: "d/m/Y",
        locale: "vn",
        maxDate: "today",
        defaultDate: [new Date().setMonth(new Date().getMonth() - 1), new Date()],
        onChange: function(selectedDates, dateStr, instance) {
            console.log('Selected dates:', selectedDates);
        }
    });

    // Khởi tạo event listeners
    initializeAllEventListeners();
});

// Hàm khởi tạo tất cả event listeners
function initializeAllEventListeners() {
    // Initialize filter toggle button
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filterSection = document.getElementById('filterSection');
    
    if (filterToggleBtn && filterSection) {
        filterToggleBtn.addEventListener('click', function() {
            filterSection.classList.toggle('show');
            filterToggleBtn.textContent = filterSection.classList.contains('show') ? 'Hide Filters' : 'Filters';
        });
    }

    // Initialize collect button
    const collectBtn = document.querySelector('button[onclick="collectNews()"]');
    if (collectBtn) {
        collectBtn.removeAttribute('onclick');
        collectBtn.addEventListener('click', collectNews);
    }

    // Initialize search button
    const searchBtn = document.querySelector('button[onclick="searchNews()"]');
    if (searchBtn) {
        searchBtn.removeAttribute('onclick');
        searchBtn.addEventListener('click', searchNews);
    }
}

// Function để render analytics khi có dữ liệu
function renderAnalytics(articles) {
    const analyticsContainer = document.getElementById('analyticsContainer');
    if (analyticsContainer && window.NewsAnalytics) {
        analyticsContainer.style.display = 'block';
        // Thêm log để debug
        console.log('Rendering analytics with articles:', articles);
        try {
            ReactDOM.render(
                React.createElement(window.NewsAnalytics, { articles: articles }),
                analyticsContainer
            );
        } catch (error) {
            console.error('Error rendering analytics:', error);
        }
    } else {
        console.error('Analytics container or component not found', {
            container: !!analyticsContainer,
            component: !!window.NewsAnalytics
        });
    }
}

// Toggle filters
function toggleFilters() {
    const filterSection = document.getElementById('filterSection');
    filterSection.classList.toggle('show');
}

// Helper function to convert date
function convertDate(dateStr) {
    const [day, month, year] = dateStr.split('/');
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

async function collectNews() {
    showLoading();
    
    try {
        const selectedSources = Array.from(document.querySelectorAll('input[name="sources"]:checked'))
            .map(cb => cb.value);
        const selectedTopics = Array.from(document.querySelectorAll('input[name="topics"]:checked'))
            .map(cb => cb.value);
    
        // Lấy giá trị từ daterangepicker
        const dateRange = $('input[name="daterange"]').val();
        const dates = dateRange.split(' - ');
        
        const requestData = {
            sources: selectedSources,
            topics: selectedTopics,
            fromdate: dates[0] ? formatDate(dates[0].trim()) : null,
            todate: dates[1] ? formatDate(dates[1].trim()) : null
        };
    
        updateDebugInfo('request', requestData);
    
        const response = await fetch('/collect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
    
        const data = await response.json();
        updateDebugInfo('response', data);
    
        if (data.success && data.data && data.data.length > 0) {
            displayArticles(data.data);
            console.log('Got data for analytics:', data.data);
            renderAnalytics(data.data);
        } else {
            throw new Error(data.error || 'No data returned');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Hàm format date mới cho daterangepicker
function formatDate(dateStr) {
    const [month, day, year] = dateStr.split('/');
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}

// Search news function
async function searchNews() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
        alert('Please enter a search term');
        return;
    }

    showLoading();
    
    try {
        const sources = Array.from(document.querySelectorAll('input[name="sources"]:checked'))
            .map(cb => cb.value);
        const topics = Array.from(document.querySelectorAll('input[name="topics"]:checked'))
            .map(cb => cb.value);

        const requestData = {
            query,
            sources: sources.length ? sources : undefined,
            topics: topics.length ? topics : undefined
        };

        updateDebugInfo('request', requestData);

        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();
        updateDebugInfo('response', data);

        if (data.success) {
            showSearchResults(data.data);
            renderAnalytics(data.data);
        } else {
            throw new Error(data.error || 'Search failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// UI Helper Functions
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function updateDebugInfo(type, data) {
    const element = document.getElementById(`${type}Debug`);
    if (element) {
        element.textContent = JSON.stringify(data, null, 2);
    }
}

function showError(message) {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="alert alert-danger">
                Error: ${escapeHtml(message)}
            </div>
        `;
    }
}

function showSearchResults(articles) {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="alert alert-${articles.length ? 'success' : 'info'}">
                ${articles.length ? `Found ${articles.length} matching articles` : 'No articles found'}
            </div>
        `;
    }
    displayArticles(articles);
}

// Display articles function
function displayArticles(articles) {
    const container = document.getElementById('articlesContainer');
    if (!container) return;

    container.innerHTML = articles.map(article => `
        <div class="col-md-4 mb-4">
            <div class="card article-card">
                <div class="card-body">
                    <h5 class="card-title">${escapeHtml(article.title)}</h5>
                    <p class="card-text description">${escapeHtml(article.description || '')}</p>
                    <div class="mt-3">
                        <p class="text-muted mb-2 small">
                            <strong>Source:</strong> ${escapeHtml(article.source)}<br>
                            <strong>Topic:</strong> ${escapeHtml(article.topic || 'N/A')}<br>
                            <strong>Date:</strong> ${escapeHtml(article.date || 'N/A')}
                        </p>
                        <a href="${escapeHtml(article.link)}" 
                           target="_blank" 
                           class="btn btn-primary btn-sm">Read More</a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Utility function
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Add styles
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .filter-section {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            opacity: 0;
        }

        .filter-section.show {
            max-height: 1000px;
            opacity: 1;
            transition: max-height 0.3s ease-in, opacity 0.3s ease-in;
        }
    </style>
`);