---
name: frontend-page-builder
description: Build complete frontend pages using reusable components, clean layouts, and consistent styling. Use for modern web interfaces.
---

# Frontend Page & Component Building

## Instructions

1. **Page Structure**
   - Semantic HTML5 layout
   - Header, main, sections, footer
   - Responsive grid or flex-based layout

2. **Component Design**
   - Reusable UI components (buttons, cards, navbars)
   - Clear component boundaries
   - Props-based or class-based variations

3. **Styling**
   - Consistent color system
   - Scalable spacing (margin/padding)
   - Typography hierarchy (headings, body, labels)
   - Dark/light theme support (if required)

4. **Responsiveness**
   - Mobile-first design
   - Breakpoints for tablet and desktop
   - Fluid layouts (no fixed widths)

5. **Interactivity**
   - Hover and focus states
   - Smooth transitions
   - Accessible keyboard navigation

## Best Practices
- Keep components small and reusable
- Avoid inline styles
- Use semantic class names
- Maintain visual consistency across pages
- Optimize for performance and accessibility

## Example Structure

```html
<main class="page">
  <header class="page-header">
    <nav class="navbar">Navbar</nav>
  </header>

  <section class="content-section">
    <div class="card">
      <h2 class="card-title">Component Title</h2>
      <p class="card-text">Reusable component content</p>
      <button class="btn-primary">Action</button>
    </div>
  </section>

  <footer class="page-footer">
    <p>© 2026</p>
  </footer>
</main>
