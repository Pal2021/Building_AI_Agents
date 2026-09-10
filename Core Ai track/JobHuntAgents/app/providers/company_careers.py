from app.providers.base import BaseSearchProvider


class FrequentlyHiringCompaniesProvider(BaseSearchProvider):
    """Static directory of official career pages for frequently hiring companies."""

    company_career_pages = (
        {
            "title": "Infosys Careers",
            "url": "https://www.infosys.com/careers.html",
            "snippet": "Official Infosys careers page.",
        },
        {
            "title": "Accenture Careers",
            "url": "https://www.accenture.com/in-en/careers",
            "snippet": "Official Accenture careers page for India.",
        },
        {
            "title": "Microsoft Careers",
            "url": "https://careers.microsoft.com/",
            "snippet": "Official Microsoft careers page.",
        },
        {
            "title": "Amazon Jobs",
            "url": "https://www.amazon.jobs/en/locations/india",
            "snippet": "Official Amazon jobs page for India.",
        },
        {
            "title": "Google Careers",
            "url": "https://www.google.com/about/careers/applications/",
            "snippet": "Official Google careers page.",
        },
        {
            "title": "IBM Careers",
            "url": "https://www.ibm.com/careers",
            "snippet": "Official IBM careers page.",
        },
        {
            "title": "Wipro Careers",
            "url": "https://careers.wipro.com/",
            "snippet": "Official Wipro careers page.",
        },
        {
            "title": "HCLTech Careers",
            "url": "https://www.hcltech.com/careers",
            "snippet": "Official HCLTech careers page.",
        },
        {
            "title": "Cognizant Careers",
            "url": "https://careers.cognizant.com/",
            "snippet": "Official Cognizant careers page.",
        },
    )

    def execute_search(self, query: str, max_results: int) -> list[dict]:
        return list(self.company_career_pages[:max_results])
