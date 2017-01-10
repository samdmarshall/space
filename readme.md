# space

space is a small tool to allow you to execute series of shell commands based on what directory you are working out of. this is mainly to cut down on the number of make/rake files I create for many of my small projects, if you also find it useful that is super.

## usage

```
space [-h|--help] [--version] [--quiet] [--verbose] [--no-ansi] [--list] [--edit] <command>
```


## configuration

space uses a file called `spaces.yml` at  `~/.config/space/spaces.yml` or will use the value of `SPACE_CONFIG` if defined.


this file should be configured as such:

```
~/path/some/folder/:
  action:
    - echo "hello, world!"
```

and if you `cd` to `~/path/some/folder/` then run `space action` you will see `hello, world!` get printed to the command line.

