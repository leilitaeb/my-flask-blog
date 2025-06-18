---
title: "Exploring the Power of CSS Grid"
author: "Jordan Smith"
date: "2023-10-27"
labels: ["css", "design", "webdev"]
---

Today we're talking about CSS Grid, which is perfect for creating the layout of this website.

The layout is defined by the `display: grid` property. We can then define columns and rows. For our site, we use:

```css
.main-container {
    display: grid;
    grid-template-columns: 1fr 3fr 1fr; /* Left, Center, Right */
    gap: 20px;
}
