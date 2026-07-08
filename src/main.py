def main():
    try:
        import pygame
    except ImportError as error:
        raise SystemExit(
            "Pygame is not installed. Run `pip install -r requirements.txt` first."
        ) from error

    from .game import Game
    from .levels import validate_all_levels

    validate_all_levels()
    pygame.init()
    try:
        Game(pygame).run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
