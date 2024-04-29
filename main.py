from socket import *
sumPrice = 0
class Laptop:
    def __init__(self, name, price):
        self.name = name
        self.price = price


with open('laptops.txt', 'r') as file:
    laptops = []
    for line in file:
        contentt = line.strip().split('-')
        name = contentt[0]
        price = contentt[1]
        sumPrice = sumPrice + float(price.strip()[1:])
        laptop = Laptop("" + name.upper(), float(price.strip()[1:]))
        laptops.append(laptop)


def fillPrice():
    print(sumPrice)
    laptops.sort(key=lambda laptop: laptop.price, reverse=True)
    html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Sorted Laptops</title>
            </head>
            <body>
                <h1>Laptops</h1>
                <ul>
            """

    for laptop in laptops:
        html_content += f"        <li><strong>Name:</strong> {laptop.name}, <strong>Price:</strong> ${laptop.price}</li>\n"
    html_content += f"            </ul>\n"
    html_content += f"            <p>The total price of all laptops  is ${sumPrice}</p>\n"
    html_content += """
                </ul>
            </body>
            </html>
            """
    with open("textSort.html", "w") as html_file:
        html_file.write(html_content.strip())


def fillName():
    laptops.sort(key=lambda laptop: laptop.name)
    html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Sorted Laptops</title>
            </head>
            <body>
                <h1>Laptops</h1>
                <ul>
            """

    for laptop in laptops:
        html_content += f"        <li><strong>Name:</strong> {laptop.name}, <strong>Price:</strong> ${laptop.price}</li>\n"

    html_content += """
                </ul>
            </body>
            </html>
            """

    with open("textSort.html", "w") as html_file:
        html_file.write(html_content.strip())


def handle_request(request):
    first_line = request.split("\r\n")[0]
    # first_line = request_lines[0]
    resource = first_line.split(" ")[1]
    temp = resource.split("/")
    if len(temp) > 2:
        if temp[2].endswith(".jpg"):
            with open(temp[2], "rb") as f:
                content = f.read()
            return content, "image/jpeg\r\n"
        elif temp[2].endswith(".png"):
            with open(temp[2], "rb") as f:
                content = f.read()
            return content, "image/png\r\n"
    else:
        if resource == "/azn":
            redirect_url = "https://www.amazon.com/"
            response = f"HTTP/1.1 307 Temporary Redirect\r\n"
            response += f"Location: {redirect_url}\r\n\r\n"
            return response.encode(), None
        elif resource == "/so":
            redirect_url = "https://stackoverflow.com/"
            response = f"HTTP/1.1 307 Temporary Redirect\r\n"
            response += f"Location: {redirect_url}\r\n\r\n"
            return response.encode(), None
        elif resource == "/bzu":
            redirect_url = "https://www.birzeit.edu/"
            response = f"HTTP/1.1 307 Temporary Redirect\r\n"
            response += f"Location: {redirect_url}\r\n\r\n"
            return response.encode(), None
        elif resource in ["/", "/index.html", "/main_en.html", "/en"]:
            resource = "main_en.html"
            with open(resource, "rb") as f:
                content = f.read()
            return content, "text/html; charset=utf-8\r\n"
        elif resource == "/ar":
            resource = "main_ar.html"
            with open(resource, "rb") as f:
                content = f.read()
            return content, "text/html; charset=utf-8\r\n"
        elif resource == "/SortByName":
            with open("textSort.html", "w") as html_file:
                html_file.write("")
            fillName()
            resource = "textSort.html"
            with open(resource, "rb") as f:
                content = f.read()
            return content, "text/html; charset=utf-8\r\n"
        elif resource == "/sortByPrice":
            with open("textSort.html", "w") as html_file:
                html_file.write("")
            fillPrice()
            resource = "textSort.html"
            with open(resource, "rb") as f:
                content = f.read()
            return content, "text/html; charset=utf-8\r\n"
        else:
            resource = resource[1:]
            if resource.endswith(".html"):
                with open(resource, "rb") as f:
                    content = f.read()
                return content, "text/html; charset=utf-8\r\n"
            elif resource.endswith(".css"):
                with open(resource, "rb") as f:
                    content = f.read()
                return content, "text/css; charset=utf-8\r\n"
            elif resource.endswith(".jpg"):
                with open(resource, "rb") as f:
                    content = f.read()
                return content, "image/jpeg\r\n"
            elif resource.endswith(".png"):
                with open(resource, "rb") as f:
                    content = f.read()
                return content, "image/png\r\n"
        return None, "text/html; charset=utf-8\r\n"


def handle_not_found(ip, port):
    with open("not_found.html", "r") as f:
        content = f.read()
    content = content.replace("{{client_ip}}", ip)
    content = content.replace("{{client_port}}", str(port))

    return content.encode()


serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(2048).decode()
        print(addr)
        print(sentence)
        ip = addr[0]
        port = addr[1]
        content, content_type = handle_request(sentence)
        print(str(content)+"----------------->content")
        if content is not None:
            if content_type is None:
                connectionSocket.send(content)
            else:
                response = "HTTP/1.1 200 OK \r\n"
                response += f"Content-Type: {content_type}"
                response += "\r\n"
                connectionSocket.send(response.encode())
                connectionSocket.send(content)
        else:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += f"Content-Type: {content_type}"
            response += "\r\n"
            content = handle_not_found(ip, port)
            connectionSocket.send(response.encode())
            connectionSocket.send(content)
        connectionSocket.close()
    except OSError:
        print("IO error")
    else:
        print("OK")

