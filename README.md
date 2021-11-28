# product-meta-analysis

## Summary
Pull data from social media sites and standalone websites to analyze what
products and ingredients are most recommended across the web.

## Supported data sources
1. **Reddit comments**. Pull top-level reddit comments and determine which
comments mention a certain brand or ingredient. In order to pull reddit comments,
you must supply a list of ids for the posts that you want to consider as well as
a list of brands or ingredients that you want to flag. See scripts/reddit for
more examples.
2. **Website ingredient cards**. Pull information from website ingredient cards
and determine which recipes mention a given ingredient. In most cases, proper
recipe schema must be implemented in order for the recipe ingredients to be obtained.
In order to pull information from website ingredient cards, you must supply a list
of urls that you want to consider as well as a list of ingredients that you want
to flag. See scripts/website for more examples.
