# Tailwind CSS Setup for myPool

This document provides instructions for using Tailwind CSS in the myPool F1 Betting Pool application.

## Quick Start

### Development Mode
To start watching for changes and auto-rebuild CSS:
```bash
npm run watch:css
```

### Production Build
To build minified CSS for production:
```bash
npm run build:css
```

## Color Palette

The project uses a modern color palette from [Coolors](https://coolors.co/c4d6b0-477998-291f1e-f64740-a3333d):

### Main Colors
- **Primary**: `#F64740` (Red Salsa) - Main action color
  - Classes: `bg-primary`, `text-primary`, `border-primary`
  - Usage: Primary buttons, CTAs, important highlights

- **Primary Dark**: `#A3333D` (Upsdell Red) - Darker variant
  - Classes: `bg-primary-dark`, `text-primary-dark`
  - Usage: Hover states, warnings, danger states

- **Secondary**: `#477998` (Queen Blue) - Secondary elements
  - Classes: `bg-secondary`, `text-secondary`
  - Usage: Secondary buttons, info states, accents

- **Dark**: `#291F1E` (Licorice) - Dark backgrounds
  - Classes: `bg-dark`, `text-dark`
  - Usage: Main background, dark sections

- **Light**: `#C4D6B0` (Tea Green) - Light accents
  - Classes: `bg-light`, `text-light`
  - Usage: Success states, highlights, light accents

### Semantic Colors
- **Success**: `#C4D6B0` (Tea Green) - `bg-success`, `text-success`
- **Info**: `#477998` (Queen Blue) - `bg-info`, `text-info`
- **Warning**: `#F64740` (Red Salsa) - `bg-warning`, `text-warning`
- **Danger**: `#A3333D` (Upsdell Red) - `bg-danger`, `text-danger`

### Podium Colors (F1 Theme)
- **Gold**: `#FFD700` - `bg-podium-gold`, `text-podium-gold`
- **Silver**: `#C0C0C0` - `bg-podium-silver`, `text-podium-silver`
- **Bronze**: `#CD7F32` - `bg-podium-bronze`, `text-podium-bronze`

### Gradients
```html
<!-- Use background-image utilities -->
<div class="bg-gradient-primary">Gradient from primary to primary-dark</div>
<div class="bg-gradient-secondary">Gradient from secondary to light</div>

<!-- Or use text gradients -->
<h1 class="text-gradient-primary">Primary gradient text</h1>
<h1 class="text-gradient-secondary">Secondary gradient text</h1>
```

### Fonts
- **Sans**: Inter (default) - Body text
- **Display**: Rajdhani - Headings and display text

Use `font-display` class for display font: `<h1 class="font-display font-black">Title</h1>`

## Custom Components

The following custom component classes are available in `static/css/input.css`:

### Buttons
```html
<!-- Base button with variants -->
<button class="btn btn-primary">Primary Action</button>
<button class="btn btn-secondary">Secondary Action</button>
<button class="btn btn-outline">Outlined Button</button>
<button class="btn btn-ghost">Ghost Button</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small Button</button>
<button class="btn btn-primary">Default Button</button>
<button class="btn btn-primary btn-lg">Large Button</button>
```

**Available Classes:**
- `btn` - Base button class (always required)
- `btn-primary` - Primary action button (coral red with hover effects)
- `btn-secondary` - Secondary button (blue grey)
- `btn-outline` - Outlined button
- `btn-ghost` - Minimal button
- `btn-sm` - Small size
- `btn-lg` - Large size

### Cards
```html
<!-- Basic card -->
<div class="card">
  <div class="card-body">
    <h3 class="card-title">Card Title</h3>
    <p>Card content goes here</p>
  </div>
</div>

<!-- Card with header and footer -->
<div class="card">
  <div class="card-header">
    <h3>Header Title</h3>
  </div>
  <div class="card-body">
    <p>Main content</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>

<!-- Competition card -->
<div class="competition-card">
  <div class="card-body">
    <div class="competition-card-year">2024</div>
    <h3 class="card-title">Season Championship</h3>
    <div class="competition-card-stats">
      <div class="stat">
        <div class="stat-value">24</div>
        <div class="stat-label">Races</div>
      </div>
      <div class="stat">
        <div class="stat-value">156</div>
        <div class="stat-label">Participants</div>
      </div>
    </div>
  </div>
</div>
```

### Forms
```html
<!-- Form group with label and input -->
<div class="form-group">
  <label class="form-label">Email Address</label>
  <input type="email" class="form-input" placeholder="your@email.com">
</div>

<!-- Textarea -->
<div class="form-group">
  <label class="form-label">Message</label>
  <textarea class="form-textarea" rows="4" placeholder="Your message"></textarea>
</div>

<!-- Select -->
<div class="form-group">
  <label class="form-label">Competition</label>
  <select class="form-select">
    <option>2024 Season</option>
    <option>2023 Season</option>
  </select>
</div>

<!-- Checkbox -->
<label class="flex items-center gap-2">
  <input type="checkbox" class="form-checkbox">
  <span>Remember me</span>
</label>
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

### Navigation
```html
<nav class="navbar">
  <div class="container py-4">
    <div class="navbar-brand">
      <div>🏎️</div>
      <span>F1 Betting Pool</span>
    </div>
    <ul class="navbar-nav">
      <li><a href="#" class="nav-link active">Competitions</a></li>
      <li><a href="#" class="nav-link">Races</a></li>
      <li><a href="#" class="nav-link">Leaderboard</a></li>
    </ul>
  </div>
</nav>
```

### Page Headers
```html
<div class="page-header">
  <h1 class="page-title">Active Competitions</h1>
  <p class="page-subtitle">Join a competition and start predicting race results</p>
</div>
```

### Leaderboard
```html
<div class="leaderboard-item">
  <div class="leaderboard-rank">1</div>
  <div class="leaderboard-user">
    <div class="leaderboard-name">John Doe</div>
    <div class="leaderboard-stats">
      <span>12 exact predictions</span>
      <span>•</span>
      <span>24 races predicted</span>
    </div>
  </div>
  <div class="leaderboard-points">486</div>
</div>
```

### Modals
```html
<div class="modal-overlay">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title">Modal Title</h2>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <p>Modal content goes here</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-ghost">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

### Loading & Empty States
```html
<!-- Loading spinner -->
<div class="loading">
  <div class="spinner"></div>
</div>

<!-- Empty state -->
<div class="empty-state">
  <div class="empty-state-icon">🏆</div>
  <h3>No competitions available</h3>
  <p>Check back later for new competitions</p>
</div>
```

## Using Tailwind in Templates

### Basic Example
```html
<div class="container mx-auto px-4">
  <h1 class="text-4xl font-display font-bold text-primary mb-4">
    F1 Betting Pool
  </h1>
  <p class="text-gray-300 mb-6">
    Place your bets and compete with friends
  </p>
  <button class="btn-primary">
    Get Started
  </button>
</div>
```

### Responsive Design
Use Tailwind's responsive prefixes:
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Cards will be 1 column on mobile, 2 on tablet, 3 on desktop -->
</div>
```

### Hover and Focus States
```html
<button class="bg-primary hover:bg-red-700 transition-colors">
  Hover Me
</button>
<input class="focus:ring-2 focus:ring-primary">
```

## Adding Custom Styles

### Method 1: Utility Classes (Preferred)
Use Tailwind's utility classes directly in templates:
```html
<div class="bg-gray-800 rounded-lg p-6 shadow-lg">
  Content here
</div>
```

### Method 2: Custom Components
Add reusable components in `static/css/input.css`:
```css
@layer components {
  .race-card {
    @apply bg-gray-800 rounded-lg p-6 border-l-4 border-primary;
  }
}
```

### Method 3: Custom Utilities
Add custom utilities in `static/css/input.css`:
```css
@layer utilities {
  .text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
}
```

## File Locations

- **Input CSS**: `static/css/input.css` - Edit this file
- **Output CSS**: `static/css/output.css` - Generated automatically (don't edit)
- **Config**: `tailwind.config.js` - Tailwind configuration
- **Templates**: Scanned paths:
  - `templates/**/*.html`
  - `betting/templates/**/*.html`
  - `static/js/**/*.js`

## Troubleshooting

### Styles not updating
1. Make sure you're running `npm run watch:css`
2. Check that your HTML file is in a scanned path
3. Rebuild with `npm run build:css`

### Class not found
1. Check if the class is a valid Tailwind class
2. Check your `tailwind.config.js` for custom configurations
3. Make sure the file containing the class is in the content array

### Build errors
1. Check `static/css/input.css` for syntax errors
2. Run `npm install` to ensure dependencies are installed
3. Check Node.js version (should be 14+)

## Migration from Legacy CSS

The project currently includes both Tailwind CSS and legacy CSS files for backwards compatibility:

- `static/css/design-system.css` - Legacy design system
- `static/css/main.css` - Legacy main styles

You can gradually migrate components to use Tailwind classes and eventually remove the legacy CSS files once the migration is complete.

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)
- [Tailwind Play](https://play.tailwindcss.com/) - Online playground
