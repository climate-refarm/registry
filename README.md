![Banner image](/docs/banner.jpg)

## Overview

**This repository tracks the current state of [Climate Refarm's](https://www.climaterefarm.com) projects and credits through a public ledger**. Our goal is to allow anyone to view and audit the lifecycle of each carbon credit.

## Terminology
- **Carbon credit**: A token that represents of `1 ton of CO₂-eq` emission reductions or removals. Each carbon credit is uniquely identified by a serial number.
- **Project**: A project that reduces or removes emissions. Projects periodically *issue* carbon credits based on their measured environmental impact. Each project has a unique identifier in this registry.
- **Ledger**: A spreadsheet for tracking carbon credits and their attributes

## Tracking Projects

Information about each of our projects can be found in the `projects` folder. Under each project ID, you'll find:
- `documentation.md`: More information about the project, such as links to external Project Description Documents (PDDs)
- `monitoring.csv`: A spreadsheet which tracks key impact metrics for each monitoring period

## Tracking Carbon Credits

- When new carbon credits are `issued`, they are added as rows on the main ledger (`ledger/main.csv`)
- When carbon credits are `retired`, their status is updated on the main ledger

> [!NOTE]
> Note that in our registry, carbon credits can have a `pre_retired` status. Pre-retirement means that the credit was sold ahead of time based on the projected impact of a project, and is equivalent to selling a carbon credit with a future vintage. When that project's next monitoring period is completed, pre-retired credits are replaced by retired credits. We made the decision to allow pre-retired credits in order to provide vital up-front funding for some of our sustainable food projects.

## Tracking our Climate Offset Portfolio

Climate Refarm allows individuals and companies to offset their emissions by purchasing offsets from a [portfolio of projects](https://www.climaterefarm.com/our-approach). This portfolio combines several different types of projects that complement each other, such as sustainable food, nature-based restoration, and conservation.

When customers purchase offsets from the portfolio, we do the following:
1. Retire offsets from the **main ledger** on their behalf
2. Add the serial numbers of the retired offsets to our **portfolio ledger**

The portfolio ledger is organied by month for convenience. For example, if you wanted to see all of the credits that were retired into the portfolio in October 2023, you could inspect the file `retirements/202310.csv`.

We maintain a running total of some portfolio impact metrics in the `summary.json` file. Among other things, these impact metrics are used calculate each user's impact on our platform.

## Verifying the Ledger

We run a number of automated checks to ensure the following:
- Credits serial numbers are unique
- Credits are never double counted
- All credits in the Climate Offset Portfolio have been properly retired
- Credit issuances from each project exactly match the emissions reductions from that project

Every update to the ledger must pass these validation checks before being submitting and reflected here.

## Development

### Commit Prefixes

Commits to this repository use prefixes to summarize what kind of change they're making:
- `code` : A code change
- `project` : A project is being created or updated
- `issue` : Credits were issued
- `retire` : Credits were retired
- `amend` : An error was corrected (e.g a typo in a serial number)
- `docs` : Documentation update

## Questions

> [!NOTE]
> If you have any questions, we're happy to help at [info@climaterefarm.com](mailto:info@climaterefarm.com). If you're a Github user, feel free to open an issue on this repository.
