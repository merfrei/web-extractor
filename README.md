
# Webpage Content Extractor Utils

Utils to extract data from webpages content

## Examples

### Working with semantic data

Extract embedded metadata from HTML markup using the semantic data extractor




```python
from extractors.semantic import SemanticData, SemanticDS

with open('page.html') as f:
    html = f.read()

semantic_data = SemanticData(html)
semantic_data._data
```




    {'jsonld': {'Product': {'@id': '215555',
       'category': 'Wonen > Verlichting > Tafellamp',
       'description': 'Met de Obvious tafellamp van BePureHome ga je terug in de tijd. Maar wel met stijl! Deze superhippe vintage lamp past perfect op een bijzettafel, als leeslamp of sfeerverlichting. De ronde vormen ademen één en al sfeer en klasse.',
       'image': 'https://mb.fcdn.nl/square340/694344/bepurehome-obvious-tafellamp.jpg',
       'name': 'BePureHome Obvious Tafellamp',
       'offers': {'@type': 'Offer',
        'availability': 'http://schema.org/InStock',
        'itemCondition': 'http://schema.org/NewCondition',
        'price': 39.95,
        'priceCurrency': 'EUR'},
       'url': 'https://www.fonq.nl/product/bepurehome-obvious-tafellamp/215555/'}},
     'microdata': {'BreadcrumbList': {'ListItem': [{'item': '/producten/categorie-wonen/',
         'name': 'Wonen'},
        {'item': '/producten/categorie-verlichting/', 'name': 'Verlichting'},
        {'item': '/producten/categorie-tafellamp/', 'name': 'Tafellamp'}]},
      'WebPage': {'AggregateRating': {'bestRating': '10',
        'ratingCount': '22.691',
        'ratingValue': '9.6'}}},
     'opengraph': {'og:app_id': '111613445595189',
      'og:description': 'Met de Obvious tafellamp van BePureHome ga je terug in de tijd. Maar wel met stijl! Deze superhippe vintage lamp past perfect op een bijzettafel, als leeslamp of sfeerverlichting. De ronde vormen ademen één en al sfeer en klasse.',
      'og:image': 'https://mb.fcdn.nl/square340/694344/bepurehome-obvious-tafellamp.jpg',
      'og:short_product_url': 'https://fonq.nl/q/215555/',
      'og:site_name': 'fonQ',
      'og:title': 'BePureHome Obvious Tafellamp',
      'og:type': 'website',
      'og:url': 'https://www.fonq.nl/product/bepurehome-obvious-tafellamp/215555/'}}




```python
jsonld_selectors = {
    'product.name': 'Product.name',
    'product.image': 'Product.image',
}

microdata_selectors = {
    'product.category': 'BreadcrumbList.ListItem[-1].name',
}

sds = SemanticDS(jsonld_selectors)  # Created using the json-ld selectors
sds.select_data(semantic_data['jsonld'])
sds.selectors = microdata_selectors  # Updated to use microdata selectors
sds.select_data(semantic_data['microdata'], clean=False)  # Update the results object without removing the old data
sds.result
```




    {'product.category': 'Tafellamp',
     'product.image': 'https://mb.fcdn.nl/square340/694344/bepurehome-obvious-tafellamp.jpg',
     'product.name': 'BePureHome Obvious Tafellamp'}



Detect selectors given the resultant value


```python
selectors = [
    ('jsonld',
     'Product.name',
     'BePureHome Obvious Tafellamp'),
    ('jsonld',
     'Product.image',
     'https://mb.fcdn.nl/square340/694344/bepurehome-obvious-tafellamp.jpg'),
    ('microdata',
     'BreadcrumbList.ListItem[2].name',
     'Tafellamp'),
]

for k, s, v in selectors:
    r = []
    SemanticDS.detect_from_value(semantic_data[k], v, r)
    print('{result} == {should_be}'.format(result=r[0], should_be=s))

```

    Product.name == Product.name
    Product.image == Product.image
    BreadcrumbList.ListItem[2].name == BreadcrumbList.ListItem[2].name


Detect a master path given a serie of resultant values so that way we can use this selector to extract all the list elements


```python
paths = ['BreadcrumbList.ListItem[0].name',
         'BreadcrumbList.ListItem[1].name']

master_path = SemanticDS.detect_master_path(*paths)
master_path
```




    'BreadcrumbList.ListItem.name'




```python
sds.selectors = {'categories': master_path}
sds.select_data(semantic_data['microdata'])
sds.result
```




    {'categories': ['Wonen', 'Verlichting', 'Tafellamp']}



### Working with XPath


```python
from extractors.html import XPathExtractor

xpe = XPathExtractor(html)

xpath = '//div[@id="productpage-container"]//h1/text()'
xpe.extract(xpath)[0]
```




    'BePureHome Obvious Tafellamp'




```python
# Extract text
xpath = '//div[@id="productpage-container"]//h1'
xpe.extract_text(xpath)[0]
```




    'BePureHome Obvious Tafellamp'



Also we can detect a XPath given a resultant value


```python
v1 = 'BePureHome Obvious Tafellamp'
xpath = xpe.get_xpath_from_value(v1)
v2 = xpe.extract_text(xpath[0])[0]
print('{} == {}'.format(v1, v2))
```

    BePureHome Obvious Tafellamp == BePureHome Obvious Tafellamp


Also we can extract a list of values given only a few of them, detecting a master path


```python
values = ['Wonen', 'Tuin & Vrije Tijd']
master_path = xpe.get_xpath_from_value(*values)
xpe.extract_text(master_path)
```




    ['Wonen',
     'Tuin & Vrije Tijd',
     'Koken & Tafelen',
     'Lifestyle',
     'Huishouden',
     'Body & Sport',
     'Baby & Kids']



-------------------------
