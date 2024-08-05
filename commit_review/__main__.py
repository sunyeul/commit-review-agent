import click

from .main import main


@click.command()
@click.option(
    "--review-point", type=str, default="可読性", help="レビューのポイントを指定します"
)
@click.option(
    "--api-choice",
    type=click.Choice(["gpt", "claude"]),
    default="gpt",
    help="使用するAPIを指定します (デフォルトは gpt)",
)
def run(review_point, api_choice):
    main(review_point, api_choice)


if __name__ == "__main__":
    run()
