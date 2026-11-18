# General Commit Strategy

Here is a quick example of how future commit messages should look like, please read the text underneath the following box, if it is the first time you read this, as it will not make sense otherwise: 

```
[#1] docs: Added commit message documentation

Added documentation explaining how we should structure commit messages, such that commit messages are proper, and easy to understand. [...]
```


In order to follow an equal commit strategy for all of us, the following commit strategy is enforced:
### 1. Meaningful commit messages 

> Commits should be meaningful, and subject lines shall not be too long (recommended: 50 characters or less, max: 70 characters)

> Descriptions can obviously be longer, but create this on a separate line.

>> If you wish to add descriptions to commit messages, you can do this in two ways:

>> Through the CLI you can do `git commit -m "subject line" -m "description"` (each `-m` adds a new paragraph).

>> If you run the commit without specifying message: `git commit` it should open some text/code editing software, where the first line is reserved for the subject line, and subsequent lines are for the description.

>> Second way is easier to handle, especially when creating larger commits.

### 2. Add issue id to the commit subject line
> When creating a new commit, please make sure to add the issue ID to the commit subject line within square brackets at the **very beginning of the subject line**

>> As an example, imagine the following commit message: `git commit -m "[#1] <subject line>` 

> Issue and pull request IDs share the same number sequence, so there is never any ambiguity between the two.

>> Essentially, if a repository has a single issue, and a PR is created for that issue, the issue will have ID #1 and the PR will have ID #2

### 3. Add commit type to the subject line
> When you're committing, remember to add the type of commit you are doing in the subject line, such that we keep track of the types of commits being pushed.

> See the list below for commit types (source: [The Art of Writing Meaningful Git Commit Messages](https://medium.com/@iambonitheuri/the-art-of-writing-meaningful-git-commit-messages-a56887a4cb49)):

>> `feat:` Commits, which adds a new feature

>> `fix:` Commits, that fixes a bug

>> `refactor:` refactored code that neither fixes a bug nor adds a feature but rewrites/restructures your code.

>> `chore:` Changes that do not relate to a fix or feature and don’t modify src or test files basically miscellaneous commits (for example, updating dependencies or modifying .gitignore file)

>> `perf:` Commits are special refactor commits, geared towards improving performance.

>> `ci:` Continuous integration related.

>> `ops:` Commits, that affect operational components like infrastructure, deployment, backup , recovery …

>> `build:` Changes that affect the build system build tool, ci pipeline, dependencies, project version, …

>> `docs:` Commits, that affect documentation, such as the README.

>> `style:` changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, etc.

>> `revert:` reverts a previous commit.

>> `test:` commits that add missing tests or correct existing tests

### 4. Use rebase to remove any intermediate commits
> If we have two features being added in the same PR, we would still like to keep the commit history of both of them. 

> In between the two major commits, we may have smaller commits though, and these commits should ideally be folded into the commit directly above.

> This can be done using `git rebase -i ` (remember to run `git fetch origin` first)

>> As an example, take the following commit history (**# are already commited messages**): 
>>```
>>a4426fb # Test workflow for code QA
>>f4e90a4 # Fix wrong argument order for uv
>>73e1e03 # use uv to run mypy and ruff
>>68766d9 # test disabling filtering for the time being
>>d d3a85c7 # Fail filtering with exit codes properly
>>e302b38 # Revert "test disabling filtering for the time being"
>>0607467 # Fix Ruff check
>>b4b245a # Remove line I used to test Ruff
>> ```

>>We can reword the actual important commits here using reword, while removing the intermediate fixing / small code changes using fixup (attaches to the commit above)
>>```
>>reword a4426fb # Test workflow for code QA
>>fixup f4e90a4 # Fix wrong argument order for uv
>>fixup 73e1e03 # use uv to run mypy and ruff
>>fixup 68766d9 # test disabling filtering for the time being
>>reword d3a85c7 # Fail filtering with exit codes properly
>>fixup e302b38 # Revert "test disabling filtering for the time being"
>>fixup 0607467 # Fix Ruff check
>>fixup b4b245a # Remove line I used to test Ruff
>> ```
>> This becomes two commits (a4426fb, d3a85c7)

>> When rewording, the commits are reran once exiting the git rebase, and your text editor should open with each commit, see visual example for the process below:
>> ![Rebase demo](demos/rebase-demo.gif)

> After creating your changes with rebase (on your own branch, obviously), the safest way to force the new changes is to use `git push --force-with-lease`, the `with-lease` makes it impossible to force push, in case your local repository does not match the origin repository. 

>This can typically happen if someone else made changes on your branch while you were rebasing, but should not occur in practice due to our branching strategy.

## Final format:
>The final format for a commit message should be as follows:
>>```
>>[#<issue-id>] <commit-type>: <subject header>
>>
>><description>
>>```

> Example:
```
[#1] docs: Added commit message documentation

Added documentation explaining how we should structure commit messages, such that commit messages are proper, and easy to understand. [...]
```

> Remember that the max recommended subject line size, including issue-id and commit type is 50 characters, with an upper limit of 70 characters.
