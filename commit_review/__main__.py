import click

from .main import main


@click.command()
@click.option(
    "--api-choice",
    type=click.Choice(["openai", "anthropic"]),
    default="openai",
    help="使用するAPIを指定します (デフォルトは openai)",
)
@click.option(
    "--review-point", type=str, default=None, help="レビューのポイントを指定します"
)
def run(api_choice, review_point):
    main(api_choice, review_point)


if __name__ == "__main__":
    run()
