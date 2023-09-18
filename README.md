![Banner image](/docs/banner.jpg)

## Overview

**This repository tracks the current state of [Climate Refarm's](https://www.climaterefarm.com) projects and credits through a public ledger**. Our goal is to allow anyone to view and audit the lifecycle of each carbon credit.

## Terminology
- :one: **Carbon credit**: A token that represents of `1 metric ton of CO₂-eq` emission reductions or removals. Each carbon credit is uniquely identified by a serial number.
- :evergreen_tree: **Project**: A project that reduces or removes emissions. Projects periodically *issue* carbon credits based on their measured environmental impact. Each project has a unique identifier in this registry.
- :clipboard: **Ledger**: A spreadsheet for tracking carbon credits and their attributes

## Tracking Projects

Information about each of our projects can be found in the `projects` folder. Under each project ID, you'll find:
- `documentation.md`: More information about the project, such as links to external Project Description Documents (PDDs)
- `monitoring.csv`: A spreadsheet which tracks key impact metrics for each monitoring period

## Tracking Carbon Credits

Carbon credits are tracked in the **main ledger** (`ledger/main.csv`):
- When new carbon credits are `issued`, they are added as rows on the main ledger
- When carbon credits are `retired`, their status is updated on the main ledger

> [!NOTE]
> Note that in our registry, carbon credits can have a `pre_retired` status. Pre-retirement means that the credit was sold ahead of time based on the projected impact of a project. This is equivalent to selling a carbon credit with a future vintage. When that project's next monitoring period is completed, pre-retired credits are always replaced by retired credits. Pre-retired credits are used to provide up-front funding for some sustainable food projects that would not be possible without it.

## Tracking our Climate Offset Portfolio

Climate Refarm allows individuals and companies to offset their emissions by purchasing offsets from a [portfolio of projects](https://www.climaterefarm.com/our-approach). This portfolio combines several complementary types of projects, such as sustainable food, nature-based restoration, and conservation.

When customers purchase offsets from the portfolio, we do the following:
1. Retire offsets from the **main ledger** on their behalf
2. Add the serial numbers of the retired offsets to our **portfolio ledger**
3. Re-calculate the total impact of portfolio with the newly retired credits included

The portfolio ledger is organized by month for convenience. For example, if you wanted to see all of the credits that were retired into the portfolio in October 2023, you could inspect the file `retirements/202310.csv`.

We maintain a running total of portfolio impact metrics in the `summary.json` file. In addition to our internal performance evaluation, these impact metrics are used calculate the impact of each customer's contribution.

## Verifying Project and Credit Accounting

We run a number of automated checks to ensure that:
- :white_check_mark: Credits serial numbers are unique
- :white_check_mark: Project IDs are unique
- :white_check_mark: Every credit is associated with a valid project ID
- :white_check_mark: Credits are not double counted
- :white_check_mark: All credits in the Climate Offset Portfolio have been properly `retired` or `pre_retired`
- :white_check_mark: Credit issuances from each project are less than or equal to emission reductions from that project

:construction: Every update to the ledger must pass these validation checks before being merged into `main`.

## Development

### Commit Prefixes

Commits to this repository use prefixes to summarize what kind of change they're making:
- `code` : A code change
- `project` : A project is being created or updated
- `issue` : Credits were issued
- `retire` : Credits were retired
- `output` : An output, like the portfolio impact, was updated
- `amend` : An error was corrected (e.g a typo in a serial number)
- `docs` : Documentation update

## Questions

> [!NOTE]
> If you have any questions, we're happy to help at [info@climaterefarm.com](mailto:info@climaterefarm.com). If you're a Github user, feel free to open an issue on this repository.
