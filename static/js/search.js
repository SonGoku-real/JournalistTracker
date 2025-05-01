document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(searchForm);
            const params = new URLSearchParams(formData);
            window.location.href = `/search/results?${params.toString()}`;
        });
    }
    
    // Handle AJAX search for instant results
    const searchInput = document.getElementById('search-query');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function() {
                performSearch();
            }, 500); // Debounce for 500ms
        });
    }
    
    // Handle filter changes
    const filterInputs = document.querySelectorAll('.search-filter');
    if (filterInputs.length > 0) {
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                performSearch();
            });
        });
    }
    
    // Initialize tabs for search results
    const resultsTabs = document.querySelectorAll('button[data-bs-toggle="tab"]');
    if (resultsTabs.length > 0) {
        resultsTabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', function(e) {
                // Update counts in tab headers
                updateResultsCountInTabs();
            });
        });
    }
});

function performSearch() {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('search-results');
    
    if (!searchForm || !resultsContainer) return;
    
    const formData = new FormData(searchForm);
    const params = new URLSearchParams(formData);
    
    // Show loading state
    resultsContainer.innerHTML = '<div class="text-center my-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Make AJAX request
    fetch(`/search/results?${params.toString()}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data);
    })
    .catch(error => {
        console.error('Error performing search:', error);
        resultsContainer.innerHTML = '<div class="alert alert-danger">An error occurred while searching. Please try again.</div>';
    });
}

function displaySearchResults(data) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    // Create tabs for different result types
    let tabsHTML = `
        <ul class="nav nav-tabs mb-4" id="results-tabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="journalists-tab" data-bs-toggle="tab" data-bs-target="#journalists" type="button" role="tab" aria-controls="journalists" aria-selected="true">
                    Journalists <span class="badge bg-primary">${data.journalists?.length || 0}</span>
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="outlets-tab" data-bs-toggle="tab" data-bs-target="#outlets" type="button" role="tab" aria-controls="outlets" aria-selected="false">
                    Outlets <span class="badge bg-primary">${data.outlets?.length || 0}</span>
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="articles-tab" data-bs-toggle="tab" data-bs-target="#articles" type="button" role="tab" aria-controls="articles" aria-selected="false">
                    Articles <span class="badge bg-primary">${data.articles?.length || 0}</span>
                </button>
            </li>
        </ul>
    `;
    
    // Create content for each tab
    let tabContentHTML = `<div class="tab-content" id="results-tabContent">`;
    
    // Journalists tab
    tabContentHTML += `<div class="tab-pane fade show active" id="journalists" role="tabpanel" aria-labelledby="journalists-tab">`;
    if (data.journalists && data.journalists.length > 0) {
        tabContentHTML += `<div class="row">`;
        data.journalists.forEach(journalist => {
            tabContentHTML += `
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <img src="${journalist.profile_image_url || '/static/img/default-profile.svg'}" alt="${journalist.name}" class="rounded-circle" width="60" height="60">
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h5 class="card-title mb-0">${journalist.name}</h5>
                                    <p class="text-muted mb-0">${journalist.outlet || 'Independent'}</p>
                                </div>
                            </div>
                            <p class="card-text">${journalist.bio?.substring(0, 100) || 'No bio available'}${journalist.bio?.length > 100 ? '...' : ''}</p>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <small class="text-muted">${journalist.location || 'Location unknown'}</small>
                                <a href="/journalists/${journalist.id}" class="btn btn-sm btn-outline-primary">View Profile</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        tabContentHTML += `</div>`;
    } else {
        tabContentHTML += `<div class="alert alert-info">No journalists found matching your search criteria.</div>`;
    }
    tabContentHTML += `</div>`;
    
    // Outlets tab
    tabContentHTML += `<div class="tab-pane fade" id="outlets" role="tabpanel" aria-labelledby="outlets-tab">`;
    if (data.outlets && data.outlets.length > 0) {
        tabContentHTML += `<div class="row">`;
        data.outlets.forEach(outlet => {
            tabContentHTML += `
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="d-flex align-items-center mb-3">
                                <div class="flex-shrink-0">
                                    <img src="${outlet.image_url || '/static/img/default-outlet.svg'}" alt="${outlet.name}" class="rounded" width="60" height="60">
                                </div>
                                <div class="flex-grow-1 ms-3">
                                    <h5 class="card-title mb-0">${outlet.name}</h5>
                                    <p class="text-muted mb-0">${outlet.country || 'International'}</p>
                                </div>
                            </div>
                            <p class="card-text">${outlet.description?.substring(0, 100) || 'No description available'}${outlet.description?.length > 100 ? '...' : ''}</p>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <small class="text-muted">${outlet.journalist_count || 0} journalists</small>
                                <a href="/outlets/${outlet.id}" class="btn btn-sm btn-outline-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        tabContentHTML += `</div>`;
    } else {
        tabContentHTML += `<div class="alert alert-info">No outlets found matching your search criteria.</div>`;
    }
    tabContentHTML += `</div>`;
    
    // Articles tab
    tabContentHTML += `<div class="tab-pane fade" id="articles" role="tabpanel" aria-labelledby="articles-tab">`;
    if (data.articles && data.articles.length > 0) {
        tabContentHTML += `<div class="list-group">`;
        data.articles.forEach(article => {
            // Determine sentiment badge class
            let sentimentClass = 'bg-secondary';
            if (article.sentiment_label === 'positive') sentimentClass = 'bg-success';
            if (article.sentiment_label === 'negative') sentimentClass = 'bg-danger';
            if (article.sentiment_label === 'neutral') sentimentClass = 'bg-info';
            
            tabContentHTML += `
                <div class="list-group-item list-group-item-action">
                    <div class="d-flex w-100 justify-content-between align-items-center">
                        <h5 class="mb-1">${article.title}</h5>
                        <span class="badge ${sentimentClass}">${article.sentiment_label || 'Unknown'}</span>
                    </div>
                    <p class="mb-1">
                        <small class="text-muted">By ${article.journalist || 'Unknown'} for ${article.outlet || 'Unknown'}</small>
                    </p>
                    <div class="d-flex justify-content-between align-items-center mt-2">
                        <small class="text-muted">${article.published_at ? new Date(article.published_at).toLocaleDateString() : 'Date unknown'}</small>
                        <a href="${article.url}" target="_blank" class="btn btn-sm btn-outline-primary">Read Article</a>
                    </div>
                </div>
            `;
        });
        tabContentHTML += `</div>`;
    } else {
        tabContentHTML += `<div class="alert alert-info">No articles found matching your search criteria.</div>`;
    }
    tabContentHTML += `</div>`;
    
    tabContentHTML += `</div>`;
    
    // Combine tabs and content
    resultsContainer.innerHTML = tabsHTML + tabContentHTML;
    
    // Initialize Bootstrap tabs
    const tabTriggers = resultsContainer.querySelectorAll('[data-bs-toggle="tab"]');
    tabTriggers.forEach(trigger => {
        new bootstrap.Tab(trigger);
    });
    
    // Update counts in tab headers
    updateResultsCountInTabs();
}

function updateResultsCountInTabs() {
    const journalistsCount = document.querySelector('#journalists .card')?.parentNode?.childElementCount || 0;
    const outletsCount = document.querySelector('#outlets .card')?.parentNode?.childElementCount || 0;
    const articlesCount = document.querySelector('#articles .list-group-item')?.parentNode?.childElementCount || 0;
    
    document.querySelector('#journalists-tab .badge').textContent = journalistsCount;
    document.querySelector('#outlets-tab .badge').textContent = outletsCount;
    document.querySelector('#articles-tab .badge').textContent = articlesCount;
}
