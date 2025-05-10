# App Icon Creation

You need to create an `icon.png` file in the `static/` directory for the PWA.

## Requirements:
- Size: 192x192 pixels
- Format: PNG
- Transparent background

## Design suggestion:
1. Background: Dark blue/black gradient
2. Main element: White luggage tag with "APT" in red, blue, and yellow blocks
3. Small airplane icon in the corner
4. Border: White or light blue outline

## You can create this using:
- Photoshop/GIMP
- Canva (free online tool)
- Figma (free design tool)
- Or use this SVG as a starting point and convert to PNG:

```svg
<svg width="192" height="192" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#000000"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="192" height="192" fill="url(#bg)" rx="32"/>
  
  <!-- Luggage tag -->
  <rect x="36" y="46" width="120" height="100" fill="#ffffff" rx="10" stroke="#000" stroke-width="3"/>
  
  <!-- Airport code letters -->
  <rect x="46" y="70" width="30" height="40" fill="#FF3B30" rx="5"/>
  <rect x="81" y="70" width="30" height="40" fill="#007AFF" rx="5"/>
  <rect x="116" y="70" width="30" height="40" fill="#FFCC00" rx="5"/>
  
  <!-- Letters -->
  <text x="61" y="95" fill="#fff" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">A</text>
  <text x="96" y="95" fill="#fff" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">P</text>
  <text x="131" y="95" fill="#fff" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">T</text>
  
  <!-- Airplane -->
  <path d="M 150,40 L 155,35 L 170,40 L 165,45 Z M 155,35 L 155,40 L 160,45 L 155,40 Z" fill="#ffffff"/>
  
  <!-- Tag string hole -->
  <circle cx="46" cy="66" r="8" fill="#ffffff" stroke="#000" stroke-width="2"/>
  <circle cx="46" cy="66" r="4" fill="#000"/>
</svg>
```

## Using the icon:
Once created, save it as `static/icon.png`. The app will automatically use it for:
- Browser tab favicon
- PWA installation icon
- "Add to Home Screen" icon on iOS/Android
