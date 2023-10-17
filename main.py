from app import create_app, cli #, context

app = create_app()
cli.register(app)
# context.add_context(myapp)
