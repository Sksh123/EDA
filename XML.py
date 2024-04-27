
from lxml import etree

def find_nodes(xml_data, path_expression):
    root = etree.fromstring(xml_data)
    nodes = root.xpath(path_expression)
    return nodes

# Function to print the traversing path
def print_traversing_path(node):
    path = [node.tag]
    parent = node.getparent()
    while parent is not None:
        path.append(parent.tag)
        parent = parent.getparent()
    path.reverse()
    print('/'.join(path))  # Print the path directly

# Example XML data
xml_data = """
<root>
    <bookstore>
        <book category="cooking">
            <title lang="en">Everyday Italian</title>
            <author>Giada De Laurentiis</author>
            <year>2005</year>
            <price>30.00</price>
        </book>
        <book category="children">
            <title lang="en">Harry Potter</title>
            <author>J.K. Rowling</author>
            <year>2005</year>
            <price>29.99</price>
        </book>
        <book category="web">
            <title lang="en">Learning XML</title>
            <author>Erik T. Ray</author>
            <year>2003</year>
            <price>39.95</price>
        </book>
        
    </bookstore>
</root>
"""

# Path expression to find all book titles
path_expression = "//book"

# Find nodes matching the path expression
matched_nodes = find_nodes(xml_data, path_expression)

# Print the titles of matched nodes along with the traversing path
for node in matched_nodes:
    print_traversing_path(node)  # Call the function to print traversing path directly
    print(f"Author: {node.xpath('author')[0].text}")  # Print the author


    




    

    # //book[@category='cooking']
    # //book[year > 2004]
    # //book[author='J.K. Rowling']/title
    # //book[number(price) < 30]/title