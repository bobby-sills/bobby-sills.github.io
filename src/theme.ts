// Theme toggle functionality
export function initTheme() {
  // Check for saved theme preference or default to dark
  const savedTheme = localStorage.getItem('theme') || 'dark';

  if (savedTheme === 'light') {
    document.documentElement.classList.add('light');
  }

  // Update background color to match theme
  updateBackgroundColor(savedTheme);
  updateFavicon(savedTheme);
}

export function toggleTheme() {
  const isLight = document.documentElement.classList.toggle('light');
  const theme = isLight ? 'light' : 'dark';
  localStorage.setItem('theme', theme);
  updateBackgroundColor(theme);
  updateFavicon(theme);
}

function updateBackgroundColor(theme: string) {
  document.documentElement.style.backgroundColor = theme === 'light' ? '#fbf1c7' : '#282828';
  document.body.style.backgroundColor = theme === 'light' ? '#fbf1c7' : '#282828';
}

function updateFavicon(theme: string) {
  const favicon = document.querySelector('link[rel="icon"]') as HTMLLinkElement;
  if (favicon) {
    favicon.href = theme === 'light' ? '/favicon-light.png' : '/favicon-dark.png';
  }
}
