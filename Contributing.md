# Contributing

Reliable Collections CLI welcomes any kind of contribution, whether it be reporting issues or sending pull requests.
When contributing to this repository abide by the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

## Code changes

### Fork

From the GitHub repository home page, select **Fork**. Forking will create a copy
of the repository under your own account. Clone this repository.

### Making changes

Be sure that you are familiar with standard git work-flows. These include editing, committing, and pushing, prior to attempting to make changes.

When making changes, the following practices are recommended:

- Commit with meaningful messages, it will help reviewers understand your work
- Start with a recent commit from the `master` branch, changes based on stale commits will be rejected
- Ensure that all new features include automated testing

### Submitting work

Once you have validated your changes and feel confident you are ready to contribute back your work, submit a pull request.

All pull requests should target the `master` branch, as it is the main development branch.

From here, follow the guidance of reviewers to get your work merged.

## Issues and questions

For questions related to Azure Service Fabric clusters, take a look at the [tag on StackOverflow](https://stackoverflow.com/questions/tagged/azure-service-fabric)
and [official documentation](https://docs.microsoft.com/en-us/azure/service-fabric/).

### General Service Fabric issues

If your issue is not specific to the Service Fabric CLI, please use the [Service Fabric issues repository](https://github.com/Azure/service-fabric-issues/issues) to report an issue.

### CLI specific issues

If your issue is relevant to the Reliable Collections CLI, please use this repositories issue tracker.

Be sure to search for similar previously reported issues prior to creating a new one.
In addition, here are some good practices to follow when reporting issues:

- Add a `+1` reaction to existing issues that are affecting you
- Include verbose output (`--debug` flag) when reporting unexpected error messages
- Include the version of rcctl installed, `pip show rcctl` will report this
- Include the version of the queryable middleware you are using on the service you are accessing
- Include the version of Service Fabric runtime for the cluster you have selected
