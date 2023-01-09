hodnoty = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
           'J', 'Q', 'K', 'A']
barvy = ['S', 'K', 'P', 'L']

balicek = [[{'hodnota': hodnota, 'barva': barva}for hodnota in hodnoty] for barva in barvy]
print(balicek)