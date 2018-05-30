from pathlib import Path


def generate_html(introduction, blog_articles, top_articles):
    current_path = Path(__file__).parent
    with open(current_path / "template.html", "r") as f:
        template = f.read()

    blog_articles_html = ""
    for article in blog_articles:
        blog_articles_html += f"""
<article>
    <a href="{article["link"]}" target="_blank">
        <img src="{article["image"]}" />
        <h4>{article["title"]}</h4>
    </a>
    <p>{article["description"]}</p>
    <div class="button">
        <a href="{article["link"]}" target="_blank">Jetzt lesen!</a>
    </div>
</article>
"""

    top_articles_html = ""
    for article in top_articles:
        top_articles_html += f"""
<article>
    <a href="{article["link"]}" target="_blank">
        <img src="{article["image"]}" />
        <h4>{article["title"]}</h4>
    </a>
    <p>{article["description"]}</p>
    <div class="button">
        <a href="{article["link"]}" target="_blank">Jetzt lesen!</a>
    </div>
</article>
"""

    # TODO: Remove it if Mailerlite fixed bug
    template = template.replace("var(--primary-color)", "rgb(21, 144, 219)")

    return template.replace("{{ introduction }}", introduction) \
        .replace("{{ blog_articles }}", blog_articles_html) \
        .replace("{{ top_articles }}", top_articles_html)


def generate_plain(introduction, blog_articles, top_articles):
    content = (
        f"{introduction}\n"
        "Leider kann diese E-Mail in deinem E-Mail-Client angezeigt werden.\n"
        "Du hast die Möglichkeit dir eine Webversion der Mail unter folgendem "
        "Link anzuzeigen: {$url}\n\n"
        "NEUE ARTIKEL AUF MEINEM BLOG\n\n"
    )

    for article in blog_articles:
        content += (
            f"{article['title']}:\n"
            f"{article['description']}\n"
            f"{article['link']}\n\n"
        )

    content += "TOP 3 ARTIKEL\n\n"

    for article in top_articles:
        content += (
            f"{article['title']}:\n"
            f"{article['description']}\n"
            f"{article['link']}\n\n"
        )

    content += (
        "Meine Webseite: https://lucas-hild.de\n"
        "Abbestellen: {$unsubscribe}"
    )

    return content
