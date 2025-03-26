## Contribution Guidelines and Conventions

The first step is to select one of the issues in this repository (or propose one).

Before adding new files or changes, let's look at the project structure:

- `.github/workflows`: CI/CD for our project; test and deploy using docker to our (planned) [website](https://grupocpq.td.utfpr.edu.br/) 
- `src`: contains the algorithms supported in this project;
- `test`: test files for the algorithms implemented in this project.s

Note that we focus on `Python` code so that (later on) we integrate the algorithm implementations in the website using [Dash]().

As stated in the README, we follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for standardizing commit messages. For example:

```
<type>(optional scope): <description>
[optional body]
[optional footer]
```

Common types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Test additions or fixes
- chore: Maintenance tasks


## General Guidance

This is a *learning project*. Your implementation should be "inspired" by these videos: [1,2]. In other words, you should implement the algorithm in a way
that it is easier (ou not so difficult) to understand cryptography. 

Resources for first-time contributors:
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Timers Only](https://www.firsttimersonly.com/)


### Contribution Process
1. Fork the repository
2. Clone your fork locally
2. Create a new branch: `git checkout -b feature-branch`
4. Make your changes, test it
5. Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork
7. Open a pull request, explain what you did.

### Testing
- Unit tests are welcome.
- Update existing tests when making changes
- You should test locally, as always; Github actions will do it too when merging (ideally on every PR).

## License
By contributing, you agree that your contributions will be licensed under the
project's [LICENSE](./LICENSE).
