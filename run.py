from skills.echo_skill import echo

if __name__ == "__main__":
    user_input = input('Sag etwas: ')
    print('Nuri sagt:', echo(user_input))
