// Main JavaScript for DocsDash

document.addEventListener('DOMContentLoaded', function() {
  // Register service worker for PWA
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/serviceworker.js')
      .then(registration => {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
      })
      .catch(error => {
        console.log('ServiceWorker registration failed: ', error);
      });
  }
  
  // Handle theme toggle
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      fetch('/auth/toggle-theme/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.dark_theme) {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      });
    });
  }
  
  // Initialize sidebar toggle
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('hidden');
      sidebar.classList.toggle('sm:block');
    });
  }
  
  // Initialize dropdown toggles
  const dropdownToggles = document.querySelectorAll('[data-dropdown-toggle]');
  dropdownToggles.forEach(toggle => {
    const targetId = toggle.getAttribute('data-dropdown-toggle');
    const target = document.getElementById(targetId);
    
    if (target) {
      toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        target.classList.toggle('hidden');
      });
    }
  });
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function() {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
      if (!menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
      }
    });
  });
  
  // Initialize tabs
  const tabLinks = document.querySelectorAll('[data-tab]');
  tabLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const tabId = this.getAttribute('data-tab');
      const tabContainer = this.closest('.tabs-container');
      
      if (tabContainer) {
        // Deactivate all tabs
        tabContainer.querySelectorAll('[data-tab]').forEach(tab => {
          tab.classList.remove('active', 'border-b-2', 'border-blue-500', 'text-blue-600');
          tab.classList.add('text-gray-500');
        });
        
        // Activate clicked tab
        this.classList.add('active', 'border-b-2', 'border-blue-500', 'text-blue-600');
        this.classList.remove('text-gray-500');
        
        // Hide all tab content
        tabContainer.querySelectorAll('.tab-content').forEach(content => {
          content.classList.add('hidden');
        });
        
        // Show selected tab content
        const tabContent = document.getElementById(tabId);
        if (tabContent) {
          tabContent.classList.remove('hidden');
        }
      }
    });
  });
  
  // Initialize collapsible sections
  const collapsibleToggles = document.querySelectorAll('[data-collapse-toggle]');
  collapsibleToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const targetId = this.getAttribute('data-collapse-toggle');
      const target = document.getElementById(targetId);
      
      if (target) {
        target.classList.toggle('hidden');
        
        // Toggle chevron icon
        const chevron = this.querySelector('.chevron');
        if (chevron) {
          chevron.classList.toggle('rotate-180');
        }
      }
    });
  });
  
  // Initialize tooltips
  const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
  tooltipTriggers.forEach(trigger => {
    trigger.addEventListener('mouseenter', function() {
      const tooltipText = this.getAttribute('data-tooltip');
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip absolute z-50 bg-gray-800 text-white text-sm px-2 py-1 rounded';
      tooltip.textContent = tooltipText;
      document.body.appendChild(tooltip);
      
      const triggerRect = this.getBoundingClientRect();
      tooltip.style.top = (triggerRect.top - tooltip.offsetHeight - 5) + 'px';
      tooltip.style.left = (triggerRect.left + (triggerRect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
    });
    
    trigger.addEventListener('mouseleave', function() {
      const tooltips = document.querySelectorAll('.tooltip');
      tooltips.forEach(tooltip => tooltip.remove());
    });
  });
  
  // Initialize modals
  const modalTriggers = document.querySelectorAll('[data-modal-target]');
  const closeModalButtons = document.querySelectorAll('[data-close-modal]');
  
  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', function() {
      const modalId = this.getAttribute('data-modal-target');
      const modal = document.getElementById(modalId);
      
      if (modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      }
    });
  });
  
  closeModalButtons.forEach(button => {
    button.addEventListener('click', function() {
      const modal = this.closest('.modal');
      if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
    });
  });
  
  // Close modals when clicking outside
  document.addEventListener('click', function(e) {
    const modals = document.querySelectorAll('.modal:not(.hidden)');
    modals.forEach(modal => {
      if (e.target === modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
    });
  });
  
  // Initialize form validation
  const forms = document.querySelectorAll('form[data-validate]');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const requiredFields = this.querySelectorAll('[required]');
      let isValid = true;
      
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('border-red-500');
          
          const errorMessage = field.getAttribute('data-error-message') || 'This field is required';
          let errorElement = field.nextElementSibling;
          
          if (!errorElement || !errorElement.classList.contains('error-message')) {
            errorElement = document.createElement('div');
            errorElement.className = 'error-message text-red-500 text-sm mt-1';
            field.parentNode.insertBefore(errorElement, field.nextSibling);
          }
          
          errorElement.textContent = errorMessage;
        } else {
          field.classList.remove('border-red-500');
          const errorElement = field.nextElementSibling;
          if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.remove();
          }
        }
      });
      
      if (!isValid) {
        e.preventDefault();
      }
    });
  });
  
  // Function to get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  // Initialize IndexedDB for offline data
  let db;
  const request = indexedDB.open('docsdash-db', 1);
  
  request.onerror = function(event) {
    console.log('Database error: ' + event.target.errorCode);
  };
  
  request.onsuccess = function(event) {
    db = event.target.result;
    console.log('Database opened successfully');
  };
  
  request.onupgradeneeded = function(event) {
    const db = event.target.result;
    db.createObjectStore('pending-patients', { keyPath: 'id', autoIncrement: true });
    db.createObjectStore('pending-appointments', { keyPath: 'id', autoIncrement: true });
  };
  
  // Handle offline form submissions
  const offlineForms = document.querySelectorAll('form[data-offline-submit]');
  offlineForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!navigator.onLine) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = {};
        
        formData.forEach((value, key) => {
          data[key] = value;
        });
        
        const storeName = this.getAttribute('data-offline-submit');
        const transaction = db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const request = store.add({ data: data, timestamp: new Date().getTime() });
        
        request.onsuccess = function() {
          console.log('Data saved for offline synchronization');
          alert('Your data has been saved locally and will be synchronized when you are back online.');
          
          // Register for background sync if supported
          if ('serviceWorker' in navigator && 'SyncManager' in window) {
            navigator.serviceWorker.ready.then(registration => {
              registration.sync.register(`sync-${storeName}`);
            });
          }
        };
      }
    });
  });
  
  // Check for online status changes
  window.addEventListener('online', function() {
    console.log('Back online');
    // Trigger sync
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      navigator.serviceWorker.ready.then(registration => {
        registration.sync.register('sync-patients');
        registration.sync.register('sync-appointments');
      });
    }
  });
  
  // Initialize PWA installation prompt
  let deferredPrompt;
  const installButton = document.getElementById('install-pwa');
  
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show the install button
    if (installButton) {
      installButton.classList.remove('hidden');
      
      installButton.addEventListener('click', () => {
        // Hide the install button
        installButton.classList.add('hidden');
        // Show the install prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the install prompt');
          } else {
            console.log('User dismissed the install prompt');
          }
          deferredPrompt = null;
        });
      });
    }
  });
});