from scorecard import models

security_categories = [
    'Compliance',
    'Process',
    'Technology'
]

security_roles = {
    'Program Manager': 'Product Security',
    'Security Escalation Contact': ''
}

security_sub_categories = [
    'Compliance Framework Collateral',
    'Secure Software Management Lifecycle Guidelines',
    'Security Capabilities',
    'Security Exception Risk'
]

statuses = {
    'implemented': 3,
    'partial': 2,
    'planned': 1,
    'none': 0,
    'not applicable': -1
}

security_capabilities = [
    [security_categories[1], security_sub_categories[1],
     "Are you accounting for OWASP top 10 Critical Vuln flaws?", ""],
    [security_categories[1], security_sub_categories[1], "Documented Security Requirements", ""],
    [security_categories[1], security_sub_categories[1], "Documented Security Test Cases", ""],
    [security_categories[1], security_sub_categories[1], "Dynamic appsec testing", ""],
    [security_categories[1], security_sub_categories[1], "Manual Code Review", ""],
    [security_categories[1], security_sub_categories[1],
     "Patterns & Reference Architecture documented for Security Features", ""],
    [security_categories[1], security_sub_categories[1], "Pen testing", ""],
    [security_categories[1], security_sub_categories[1], "Prior to Packaging, Vuln/Malware/Anti-Virus scanning", ""],
    [security_categories[1], security_sub_categories[1], "Risk Assessment & Business Impact Analysis", ""],
    [security_categories[1], security_sub_categories[1], "Secure Coding Guide", ""],
    [security_categories[1], security_sub_categories[1], "Security Architecture", ""],
    [security_categories[1], security_sub_categories[1], "Security Awareness Training", ""],
    [security_categories[1], security_sub_categories[1], "Security Test Plan", ""],
    [security_categories[1], security_sub_categories[1], "Static Code Analysis", ""],
    [security_categories[1], security_sub_categories[1], "Threat Model", ""],
    [security_categories[1], security_sub_categories[3], "Overall Risk Score",
     "http://prodsec.redhat.com/static/supported.html"],
    [security_categories[2], security_sub_categories[2],
     "All Logs Use Common Logging and Can Be Sent Externally, Encrypted", ""],
    [security_categories[2], security_sub_categories[2], "Cryptographic Agility without Recompiling", ""],
    [security_categories[2], security_sub_categories[2], "Has a Known FirewallD Configuration", "AC-17(9), SC-7(12)"],
    [security_categories[2], security_sub_categories[2],
     "Instructions Exist to Enable SSL/TLS or Is Enabled by Default", "AC-17(2), CM-7"],
    [security_categories[2], security_sub_categories[2], "Supports Attestation with SCAP", "CM-6"],
    [security_categories[2], security_sub_categories[2], "Supports Auditing Security Events",
     "AC-17(7), AU-1(b), AU-2(a), AU-2(c), AU-2(d), AU-2(4), AU-6(9), AU-12(a), AU-12(c), IR-5"],
    [security_categories[2], security_sub_categories[2], "Supports Centralized Logging", "AU-6, AU-3(2), SI-4(2)"],
    [security_categories[2], security_sub_categories[2], "Supports Identity Management", ""],
    [security_categories[2], security_sub_categories[2], "Supports Kerberos Based SSO", ""],
    [security_categories[2], security_sub_categories[2], "Works with FIPS Enabled", "AC-17(2)"],
    [security_categories[2], security_sub_categories[2], "Works with SELINUX Set to Enforcing",
     "AC-3, AC-3(3), AC-3(4), AC-4, AC-6, AU-9, SI-6(a), SC-7(12)"],
    [security_categories[0], security_sub_categories[0], "C2S Benchmarks", ""],
    [security_categories[0], security_sub_categories[0], "Common Criteria", ""],
    [security_categories[0], security_sub_categories[0], "FIPS 140-2", ""],
    [security_categories[0], security_sub_categories[0], "FedRAMP", ""],
    [security_categories[0], security_sub_categories[0], "HIPAA", ""],
    [security_categories[0], security_sub_categories[0], "ISO 27001:2013", ""],
    [security_categories[0], security_sub_categories[0], "NIST 800-53", ""],
    [security_categories[0], security_sub_categories[0], "PCI-DSSv3", ""]
]


def set_up_data():

    # Categories
    for category in security_categories:
        models.SecurityCategory.objects.get_or_create(name=category)

    # Subcategories
    for sub_category in security_sub_categories:
        models.SecuritySubCategory.objects.get_or_create(name=sub_category)

    # Roles
    for role in security_roles.keys():
        models.SecurityRole.objects.get_or_create(description=role, function=security_roles[role])

    # Statuses
    for status in statuses.keys():
        models.Status.objects.get_or_create(name=status, value=statuses[status])

    # Capabilities
    for capability in security_capabilities:
        category = models.SecurityCategory.objects.get(name=capability[0])
        sub_category = models.SecuritySubCategory.objects.get(name=capability[1])
        models.SecurityCapability.objects.get_or_create(name=capability[2], supporting_controls=capability[3],
                                                        category=category, sub_category=sub_category)
