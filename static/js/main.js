// Leonardo AI Clone - Main JavaScript

// Global variables
let currentSessionId = null;
let selectedImageId = null;
let hasFilterApplied = false;

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize event listeners
    initializeEventListeners();

    // Display sample images on initial load
    displaySampleImages();

    // Initialize dropdown values
    initializeDropdowns();
});

/**
 * Initialize dropdown values
 */
function initializeDropdowns() {
    // Set default values for dropdowns
    const modelDropdown = document.querySelector('.sidebar-section:nth-child(1) .dropdown-container');
    if (modelDropdown) {
        const modelName = "Flux Dev";
        const modelType = "Flux";

        // Update header text
        const header = modelDropdown.querySelector('.dropdown-header');
        if (header) {
            const nameElement = header.querySelector('.model-name');
            const typeElement = header.querySelector('.model-type');

            if (nameElement) nameElement.textContent = modelName;
            if (typeElement) typeElement.textContent = modelType;
        }

        // Store selected value
        modelDropdown.setAttribute('data-selected', modelName);
    }

    // Format Enhance dropdown
    const formatDropdown = document.querySelector('.sidebar-section:nth-child(2) .dropdown-container');
    if (formatDropdown) {
        const formatName = "Auto";

        // Update header text
        const header = formatDropdown.querySelector('.dropdown-header');
        if (header) {
            const nameElement = header.querySelector('.model-name');
            if (nameElement) nameElement.textContent = formatName;
        }

        // Store selected value
        formatDropdown.setAttribute('data-selected', formatName);
    }

    // Style dropdown
    const styleDropdown = document.querySelector('.sidebar-section:nth-child(3) .dropdown-container');
    if (styleDropdown) {
        const styleName = "Dynamic";

        // Update header text
        const header = styleDropdown.querySelector('.dropdown-header');
        if (header) {
            const nameElement = header.querySelector('.model-name');
            if (nameElement) nameElement.textContent = styleName;
        }

        // Store selected value
        styleDropdown.setAttribute('data-selected', styleName);
    }
}

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Generate button
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateImages);
    }

    // First, clean up any existing dropdown menus to avoid duplicates
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        if (menu.querySelector('.dropdown-search')) {
            menu.remove();
        }
    });

    // Dropdown menus with search functionality
    const dropdownContainers = document.querySelectorAll('.dropdown-container');

    // First, remove all existing dropdown menus to start fresh
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.remove();
    });

    // Now create new dropdown menus for each container
    dropdownContainers.forEach((container, index) => {
        // Create a completely new dropdown menu
        const menu = document.createElement('div');
        menu.className = 'dropdown-menu';
        menu.id = `dropdown-menu-${index}`;
        menu.style.zIndex = 1000 - index; // Ensure proper stacking

        // Set initial display to none
        menu.style.display = 'none';

        // Add a data attribute to identify which section this belongs to
        const sectionTitle = container.closest('.sidebar-section')?.querySelector('h3')?.textContent || `Section ${index}`;
        menu.setAttribute('data-section', sectionTitle);

        // Append to container
        container.appendChild(menu);

        // Log for debugging
        console.log(`Created dropdown menu #${index} for section: ${menu.getAttribute('data-section')}`);

        const header = container.querySelector('.dropdown-header');

        // Store original dropdown items for reference
        const originalItems = Array.from(container.querySelectorAll('.dropdown-item'));

        // Set initial selected value
        const firstItem = container.querySelector('.dropdown-item');
        if (firstItem) {
            const value = firstItem.getAttribute('data-value');
            container.setAttribute('data-selected', value);
        }

        // Add search input to each dropdown
        // Clear the menu first
        menu.innerHTML = '';

        // Create search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'dropdown-search';
        searchInput.placeholder = 'Search...';
        searchInput.autocomplete = 'off';

        // Create a wrapper for items
        const itemsWrapper = document.createElement('div');
        itemsWrapper.className = 'dropdown-items';

        // Clone and add items to the wrapper
        originalItems.forEach(item => {
            // Create a completely new item instead of cloning
            const newItem = document.createElement('div');
            newItem.className = 'dropdown-item';
            newItem.setAttribute('data-value', item.getAttribute('data-value'));

            // Create model name element
            const modelNameEl = document.createElement('div');
            modelNameEl.className = 'model-name';
            modelNameEl.textContent = item.querySelector('.model-name').textContent;

            // Create model type element if it exists
            const modelTypeEl = item.querySelector('.model-type');
            if (modelTypeEl) {
                const newModelTypeEl = document.createElement('div');
                newModelTypeEl.className = 'model-type';
                newModelTypeEl.textContent = modelTypeEl.textContent;
                newItem.appendChild(newModelTypeEl);
            }

            // Add model name after model type (for styling purposes)
            newItem.appendChild(modelNameEl);

            // Add the new item to the wrapper
            itemsWrapper.appendChild(newItem);

            // Add click event to the new item
            newItem.addEventListener('click', function(e) {
                e.stopPropagation();

                const value = this.getAttribute('data-value');
                const modelName = this.querySelector('.model-name').textContent;
                const modelType = this.querySelector('.model-type')?.textContent;

                // Update header text
                const headerNameElement = header.querySelector('.model-name');
                const headerTypeElement = header.querySelector('.model-type');

                if (headerNameElement) headerNameElement.textContent = modelName;
                if (modelType && headerTypeElement) headerTypeElement.textContent = modelType;

                // Close dropdown
                container.classList.remove('active');
                menu.style.display = 'none';

                // Store selected value
                container.setAttribute('data-selected', value);

                // Log selection
                console.log('Selected:', value);
            });
        });

        // Add elements to menu
        menu.appendChild(searchInput);
        menu.appendChild(itemsWrapper);

        // Add search functionality
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const dropdownItems = itemsWrapper.querySelectorAll('.dropdown-item');
            let hasResults = false;

            dropdownItems.forEach(item => {
                const modelName = item.querySelector('.model-name').textContent.toLowerCase();
                const modelType = item.querySelector('.model-type')?.textContent?.toLowerCase() || '';

                if (modelName.includes(searchTerm) || modelType.includes(searchTerm)) {
                    item.style.display = 'flex';
                    // Highlight matching text
                    if (searchTerm.length > 0) {
                        const nameElement = item.querySelector('.model-name');
                        const typeElement = item.querySelector('.model-type');

                        // Reset content first
                        nameElement.innerHTML = modelName;
                        if (typeElement) typeElement.innerHTML = modelType || '';

                        // Highlight matching text
                        if (modelName.includes(searchTerm)) {
                            const highlightedText = modelName.replace(
                                new RegExp(searchTerm, 'gi'),
                                match => `<span style="background-color: rgba(255,51,102,0.3); padding: 0 2px;">${match}</span>`
                            );
                            nameElement.innerHTML = highlightedText;
                        }

                        if (modelType && modelType.includes(searchTerm)) {
                            const highlightedText = modelType.replace(
                                new RegExp(searchTerm, 'gi'),
                                match => `<span style="background-color: rgba(255,51,102,0.3); padding: 0 2px;">${match}</span>`
                            );
                            if (typeElement) typeElement.innerHTML = highlightedText;
                        }
                    }
                    hasResults = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // Show a "no results" message if needed
            let noResultsMsg = itemsWrapper.querySelector('.no-results-message');
            if (!hasResults) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.className = 'no-results-message';
                    noResultsMsg.style.padding = '10px';
                    noResultsMsg.style.textAlign = 'center';
                    noResultsMsg.style.color = 'var(--secondary-text)';
                    itemsWrapper.appendChild(noResultsMsg);
                }
                noResultsMsg.textContent = `No results for "${searchTerm}"`;
                noResultsMsg.style.display = 'block';
            } else if (noResultsMsg) {
                noResultsMsg.style.display = 'none';
            }
        });

        // Prevent search input from closing dropdown and focus on click
        searchInput.addEventListener('click', function(e) {
            e.stopPropagation();
            this.focus();
        });

        // Toggle dropdown on header click
        header.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent event from bubbling up

            console.log('Header clicked for dropdown:', container.id || index);

            // Close all other dropdowns and their menus
            document.querySelectorAll('.dropdown-container').forEach(c => {
                if (c !== container) {
                    c.classList.remove('active');
                    const otherMenu = c.querySelector('.dropdown-menu');
                    if (otherMenu) {
                        otherMenu.style.display = 'none';
                    }
                }
            });

            // Toggle current dropdown
            const isActive = container.classList.toggle('active');
            console.log('Dropdown active state:', isActive);

            // Explicitly show/hide the menu
            if (isActive) {
                menu.style.display = 'block';
                console.log('Menu should be visible now:', menu.id);

                // Focus search input when dropdown opens
                const searchInput = menu.querySelector('.dropdown-search');
                if (searchInput) {
                    setTimeout(() => {
                        searchInput.focus();
                        console.log('Search input focused');
                    }, 100);
                }
            } else {
                menu.style.display = 'none';
                console.log('Menu should be hidden now:', menu.id);
            }
        });

        // Handle item selection for original items
        originalItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent event from bubbling up

                const value = this.getAttribute('data-value');
                const modelName = this.querySelector('.model-name').textContent;
                const modelType = this.querySelector('.model-type')?.textContent;

                // Update header text
                header.querySelector('.model-name').textContent = modelName;
                if (modelType && header.querySelector('.model-type')) {
                    header.querySelector('.model-type').textContent = modelType;
                }

                // Close dropdown
                container.classList.remove('active');

                // Store selected value
                container.setAttribute('data-selected', value);

                // Log selection
                console.log('Selected:', value);
            });
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        console.log('Document clicked, checking dropdowns');
        document.querySelectorAll('.dropdown-container').forEach(container => {
            if (!container.contains(event.target)) {
                container.classList.remove('active');
                const menu = container.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.display = 'none';
                    console.log('Closing dropdown menu:', menu.id);
                }
            }
        });
    });

    // Dimension options
    const dimensionOptions = document.querySelectorAll('.dimension-option');
    dimensionOptions.forEach(option => {
        option.addEventListener('click', function() {
            dimensionOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Image count options
    const countOptions = document.querySelectorAll('.count-option');
    countOptions.forEach(option => {
        option.addEventListener('click', function() {
            if (!this.querySelector('.fa-ellipsis-h')) {
                countOptions.forEach(opt => opt.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // Toggle switches
    const legacyModeToggle = document.getElementById('legacyModeToggle');
    if (legacyModeToggle) {
        legacyModeToggle.addEventListener('change', function() {
            console.log('Legacy Mode:', this.checked ? 'Off' : 'On');
        });
    }

    const privateModeToggle = document.getElementById('privateModeToggle');
    if (privateModeToggle) {
        privateModeToggle.addEventListener('change', function() {
            console.log('Private Mode:', this.checked ? 'On' : 'Off');
        });
    }

    // Advanced settings sliders
    const guidanceScaleSlider = document.getElementById('guidanceScale');
    const guidanceScaleValue = document.getElementById('guidanceScaleValue');
    if (guidanceScaleSlider && guidanceScaleValue) {
        guidanceScaleSlider.addEventListener('input', function() {
            guidanceScaleValue.textContent = this.value;
        });
    }

    const stepsSlider = document.getElementById('steps');
    const stepsValue = document.getElementById('stepsValue');
    if (stepsSlider && stepsValue) {
        stepsSlider.addEventListener('input', function() {
            stepsValue.textContent = this.value;
        });
    }

    // Prompt tabs
    const promptTabs = document.querySelectorAll('.prompt-tab');
    promptTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            if (!this.classList.contains('new')) {
                promptTabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // Chat bubble
    const chatBubble = document.querySelector('.chat-bubble');
    if (chatBubble) {
        chatBubble.addEventListener('click', function() {
            alert('AI Assistant is not available in this demo.');
        });
    }
}

/**
 * Display sample images on initial load
 */
function displaySampleImages() {
    // Sample image data - in a real app, these would come from the server
    const sampleImages = [
        {
            prompt: 'A dimly lit, cozy living room with warm ambient light—perhaps a floor lamp glowing softly in the corner. The walls are...',
            style: 'Dynamic',
            resolution: '1024x1024px',
            model: 'Flux Dev'
        },
        {
            prompt: 'A dimly lit, cozy living room with warm ambient light—perhaps a floor lamp glowing softly in the corner. The walls are...',
            style: 'Dynamic',
            resolution: '1024x1024px',
            model: 'Flux Dev'
        },
        {
            prompt: 'A dimly lit, cozy living room with warm ambient light—perhaps a floor lamp glowing softly in the corner. The walls are...',
            style: 'Dynamic',
            resolution: '1024x1024px',
            model: 'Flux Dev'
        },
        {
            prompt: 'A dimly lit, cozy living room with warm ambient light—perhaps a floor lamp glowing softly in the corner. The walls are...',
            style: 'Dynamic',
            resolution: '1024x1024px',
            model: 'Flux Dev'
        }
    ];

    // Create placeholder images
    const imageGrid = document.getElementById('imageGrid');
    if (imageGrid) {
        imageGrid.innerHTML = '';

        // Create a row for the prompt
        const promptRow = document.createElement('div');
        promptRow.className = 'mb-3';
        promptRow.style.gridColumn = '1 / -1';

        const promptText = document.createElement('div');
        promptText.className = 'image-score';
        promptText.innerHTML = `<strong>Score:</strong> ${sampleImages[0].prompt}`;

        const promptControls = document.createElement('div');
        promptControls.className = 'control-buttons mt-2';
        promptControls.innerHTML = `
            <button class="control-button"><i class="fas fa-plus"></i></button>
            <button class="control-button"><i class="fas fa-palette"></i></button>
            <button class="control-button"><i class="fas fa-magic"></i></button>
            <button class="control-button"><i class="fas fa-expand"></i></button>
            <button class="control-button"><i class="fas fa-ellipsis-h"></i></button>
        `;

        promptRow.appendChild(promptText);
        promptRow.appendChild(promptControls);
        imageGrid.appendChild(promptRow);

        // Create image cards
        sampleImages.forEach((image, index) => {
            const card = createImageCard(index, image);
            imageGrid.appendChild(card);
        });
    }
}

/**
 * Create an image card element
 */
function createImageCard(index, imageData) {
    // Create image card
    const card = document.createElement('div');
    card.className = 'image-card';
    card.dataset.imageId = index;

    // Create a placeholder image with gradient
    const img = document.createElement('img');
    img.src = createPlaceholderImage(index);
    img.alt = 'Generated Image ' + (index + 1);

    // Create image controls
    const controls = document.createElement('div');
    controls.className = 'image-controls';

    const score = document.createElement('div');
    score.className = 'image-score';
    score.innerHTML = `<i class="fas fa-${index % 2 === 0 ? 'star' : 'heart'}"></i> <i class="fas fa-${index % 2 === 0 ? 'dynamic' : 'palette'}"></i> <i class="fas fa-${index % 2 === 0 ? '4' : '1'}"></i>`;

    const buttons = document.createElement('div');
    buttons.className = 'control-buttons';
    buttons.innerHTML = `
        <button class="control-button"><i class="fas fa-expand"></i></button>
        <button class="control-button"><i class="fas fa-ellipsis-h"></i></button>
    `;

    // Append elements
    controls.appendChild(score);
    controls.appendChild(buttons);
    card.appendChild(img);
    card.appendChild(controls);

    // Add click event
    card.addEventListener('click', () => selectImage(index, img.src));

    return card;
}

/**
 * Create a placeholder gradient image
 */
function createPlaceholderImage(index) {
    // In a real app, this would be a real image URL
    // For this demo, we'll use a data URL with a gradient
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');

    // Create gradient based on index
    let gradient;
    switch (index % 4) {
        case 0:
            gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#3a1c71');
            gradient.addColorStop(0.5, '#d76d77');
            gradient.addColorStop(1, '#ffaf7b');
            break;
        case 1:
            gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#4b6cb7');
            gradient.addColorStop(1, '#182848');
            break;
        case 2:
            gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#f46b45');
            gradient.addColorStop(1, '#eea849');
            break;
        case 3:
            gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#43cea2');
            gradient.addColorStop(1, '#185a9d');
            break;
    }

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    return canvas.toDataURL();
}

/**
 * Generate images based on the form inputs
 */
function generateImages() {
    const promptInput = document.getElementById('promptInput');
    const prompt = promptInput.value.trim();

    if (!prompt) {
        alert('Please enter a prompt first.');
        return;
    }

    // Show loading indicator
    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.classList.remove('d-none');

    // Hide previous results
    const generatedImages = document.getElementById('generatedImages');
    generatedImages.style.display = 'none';

    // Get selected dimension
    let width = 1024;
    let height = 576;
    const activeDimension = document.querySelector('.dimension-option.active');
    if (activeDimension) {
        const ratio = activeDimension.querySelector('.ratio').textContent;
        if (ratio === '3:4') {
            width = 768;
            height = 1024;
        } else if (ratio === '1:1') {
            width = 1024;
            height = 1024;
        } else if (ratio === '16:9') {
            width = 1024;
            height = 576;
        }
    }

    // Get number of images
    let numImages = 1;
    const activeCount = document.querySelector('.count-option.active');
    if (activeCount && !activeCount.querySelector('.fa-ellipsis-h')) {
        numImages = parseInt(activeCount.textContent) || 1;
    }

    // Get selected model
    let model = 'Flux Dev';
    const modelContainer = document.querySelector('.sidebar-section:nth-child(1) .dropdown-container');
    if (modelContainer && modelContainer.getAttribute('data-selected')) {
        model = modelContainer.getAttribute('data-selected');
    }

    // Get selected format enhance
    let formatEnhance = 'Auto';
    const formatContainer = document.querySelector('.sidebar-section:nth-child(2) .dropdown-container');
    if (formatContainer && formatContainer.getAttribute('data-selected')) {
        formatEnhance = formatContainer.getAttribute('data-selected');
    }

    // Get selected style
    let style = 'Dynamic';
    const styleContainer = document.querySelector('.sidebar-section:nth-child(3) .dropdown-container');
    if (styleContainer && styleContainer.getAttribute('data-selected')) {
        style = styleContainer.getAttribute('data-selected');
    }

    // Check if private mode is enabled
    const privateMode = document.getElementById('privateModeToggle').checked;

    // Get advanced settings
    let steps = 50;
    const stepsSlider = document.getElementById('steps');
    if (stepsSlider) {
        steps = parseInt(stepsSlider.value);
    }

    let guidanceScale = 7.5;
    const guidanceScaleSlider = document.getElementById('guidanceScale');
    if (guidanceScaleSlider) {
        guidanceScale = parseFloat(guidanceScaleSlider.value);
    }

    let seed = -1;
    const seedInput = document.getElementById('seed');
    if (seedInput) {
        seed = parseInt(seedInput.value);
    }

    let negativePrompt = '';
    const negativePromptInput = document.getElementById('negativePrompt');
    if (negativePromptInput) {
        negativePrompt = negativePromptInput.value.trim();
    }

    // Create form data
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('num_images', numImages);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('steps', steps);
    formData.append('guidance_scale', guidanceScale);
    formData.append('seed', seed);
    formData.append('model', model);
    formData.append('format_enhance', formatEnhance);
    formData.append('style', style);
    formData.append('private_mode', privateMode);
    formData.append('negative_prompt', negativePrompt);

    // Update token cost display
    const tokenCost = (numImages * 0.4).toFixed(2);
    document.querySelector('.generate-button span').textContent = `$${tokenCost}`;

    // Send request to server
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Store session ID
            currentSessionId = data.session_id;

            // Display generated images
            displayGeneratedImages(data.images, prompt);

            // Update token balance display
            if (data.remaining_tokens !== undefined) {
                document.querySelector('.token-balance').innerHTML = `<i class="fas fa-coins"></i> ${data.remaining_tokens.toFixed(1)}`;
            }

            // Hide loading indicator
            loadingIndicator.classList.add('d-none');

            // Show generated images section
            generatedImages.style.display = 'block';
        } else {
            alert('Error generating images: ' + data.error);
            loadingIndicator.classList.add('d-none');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating images.');
        loadingIndicator.classList.add('d-none');
    });
}

/**
 * Display the generated images in the grid
 */
function displayGeneratedImages(images, prompt) {
    const imageGrid = document.getElementById('imageGrid');
    imageGrid.innerHTML = '';

    // Get selected model and style
    let model = 'Flux Dev';
    const modelContainer = document.querySelector('.sidebar-section:nth-child(1) .dropdown-container');
    if (modelContainer && modelContainer.getAttribute('data-selected')) {
        model = modelContainer.getAttribute('data-selected');
    }

    let style = 'Dynamic';
    const styleContainer = document.querySelector('.sidebar-section:nth-child(3) .dropdown-container');
    if (styleContainer && styleContainer.getAttribute('data-selected')) {
        style = styleContainer.getAttribute('data-selected');
    }

    // Create a row for the prompt
    const promptRow = document.createElement('div');
    promptRow.className = 'mb-3';
    promptRow.style.gridColumn = '1 / -1';

    const promptText = document.createElement('div');
    promptText.className = 'image-score';
    promptText.innerHTML = `<strong>Score:</strong> ${prompt}`;

    const promptControls = document.createElement('div');
    promptControls.className = 'control-buttons mt-2';
    promptControls.innerHTML = `
        <button class="control-button"><i class="fas fa-plus"></i></button>
        <button class="control-button"><i class="fas fa-palette"></i></button>
        <button class="control-button"><i class="fas fa-magic"></i></button>
        <button class="control-button"><i class="fas fa-expand"></i></button>
        <button class="control-button"><i class="fas fa-ellipsis-h"></i></button>
    `;

    promptRow.appendChild(promptText);
    promptRow.appendChild(promptControls);
    imageGrid.appendChild(promptRow);

    images.forEach((imageUrl, index) => {
        // Create image card
        const card = document.createElement('div');
        card.className = 'image-card';
        card.dataset.imageId = index;

        // Create image
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = 'Generated Image ' + (index + 1);

        // Create image controls
        const controls = document.createElement('div');
        controls.className = 'image-controls';

        // Get dimensions from active option
        let dimensions = '1024x576px';
        const activeDimension = document.querySelector('.dimension-option.active');
        if (activeDimension) {
            const pixels = activeDimension.querySelector('.pixels');
            if (pixels) {
                dimensions = pixels.textContent;
            }
        }

        const score = document.createElement('div');
        score.className = 'image-score';
        score.innerHTML = `
            <i class="fas fa-star"></i>
            <span class="model-badge">${model}</span>
            <span class="style-badge">${style}</span>
            <span class="resolution-badge">${dimensions}</span>
        `;

        const buttons = document.createElement('div');
        buttons.className = 'control-buttons';
        buttons.innerHTML = `
            <button class="control-button" title="Download"><i class="fas fa-download"></i></button>
            <button class="control-button" title="Expand"><i class="fas fa-expand"></i></button>
            <button class="control-button" title="More options"><i class="fas fa-ellipsis-h"></i></button>
        `;

        // Add download functionality
        const downloadBtn = buttons.querySelector('.fa-download').parentElement;
        downloadBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            downloadImage(index, imageUrl);
        });

        // Append elements
        controls.appendChild(score);
        controls.appendChild(buttons);
        card.appendChild(img);
        card.appendChild(controls);

        // Add click event
        card.addEventListener('click', () => selectImage(index, imageUrl));

        imageGrid.appendChild(card);
    });
}

/**
 * Select an image for editing
 */
function selectImage(imageId, imageUrl) {
    // Update selected image
    selectedImageId = imageId;
    hasFilterApplied = false;

    // Update UI to show selected image
    const imageCards = document.querySelectorAll('.image-card');
    imageCards.forEach(card => {
        if (parseInt(card.dataset.imageId) === imageId) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });

    // In the Leonardo AI interface, clicking an image might show a modal or expand it
    // For this demo, we'll just log the selection
    console.log('Selected image:', imageId, imageUrl);
}

/**
 * Download the current image
 */
function downloadImage(imageId, imageUrl) {
    // Create a temporary link and click it
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `leonardo_ai_image_${imageId}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
