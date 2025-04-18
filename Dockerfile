FROM ruby:3.0
LABEL maintainer="Your teammate"         # John Doe
WORKDIR /app
COPY . /app
RUN bundle install
CMD ["rails", "server"] # Startup command for MyAwesomeService.
