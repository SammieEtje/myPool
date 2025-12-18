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

## Configuration

### Theme Colors
The project uses F1-themed colors configured in `tailwind.config.js`:

- **Primary**: `#DC0000` (F1 Red) - Use with `bg-primary`, `text-primary`, `border-primary`
- **Secondary**: `#15151E` (Dark background) - Use with `bg-secondary`
- **Accent Colors**:
  - Gold: `#FFD700` - Use with `bg-accent-gold`
  - Silver: `#C0C0C0` - Use with `bg-accent-silver`
  - Bronze: `#CD7F32` - Use with `bg-accent-bronze`

### Fonts
- **Sans**: Inter (default)
- **Display**: Rajdhani (for headings)

Use `font-display` class for display font: `<h1 class="font-display">Title</h1>`

## Custom Components

The following custom component classes are available in `static/css/input.css`:

### Buttons
- `btn-primary` - Primary button (red background)
- `btn-secondary` - Secondary button (gray background)
- `btn-outline` - Outline button (red border)

Example:
```html
<button class="btn-primary">Join Competition</button>
<button class="btn-outline">View Details</button>
```

### Cards
- `card` - Standard card component

Example:
```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content</p>
</div>
```

### Forms
- `input-field` - Styled form input

Example:
```html
<input type="text" class="input-field" placeholder="Enter email">
```

### Badges
- `badge` - Base badge style
- `badge-primary` - Red badge
- `badge-success` - Green badge
- `badge-warning` - Yellow badge
- `badge-error` - Red error badge

Example:
```html
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Pending</span>
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
