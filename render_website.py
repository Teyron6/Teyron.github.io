import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

def on_reload():
    with open ('./meta_data.json', 'r', encoding="utf8") as file:
        meta_data = json.load(file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html']),
        )
    template = env.get_template('template.html')

    books_on_page = 20
    chunked_books = list(chunked(meta_data, books_on_page))

    for num, chunked_book in enumerate(chunked_books, 1):
        render_output = template.render(books=chunked_book,
                                        current_page=num,
                                        amount_of_pages=len(chunked_books),
                                        )

        with open(f'./pages/index{num}.html', 'w', encoding='utf8') as file:
            file.write(render_output)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='./pages/index1.html')


if __name__ == '__main__':
    main()