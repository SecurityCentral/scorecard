from scorecard import models, scoring

security_categories = [
    scoring.COMPLIANCE,
    scoring.PROCESS,
    scoring.TECHNOLOGY
]

security_roles = {
    'Program Manager': 'Product Security',
    'Security Escalation Contact': ''
}

COMPLIANCE_FRAMEWORK_COLLATERAL = "Compliance Framework Collateral"
SEC_SFTWR_MNGMNT_LFCYCL_GDLNS = "Secure Software Management Lifecycle Guidelines"
SECURITY_CAPABILITIES = "Security Capabilities"
SECURITY_EXCEPTION_RISK = "Security Exception Risk"

security_sub_categories = [
    COMPLIANCE_FRAMEWORK_COLLATERAL,
    SEC_SFTWR_MNGMNT_LFCYCL_GDLNS,
    SECURITY_CAPABILITIES,
    SECURITY_EXCEPTION_RISK
]

statuses = {
    'implemented': 3,
    'partial': 2,
    'planned': 1,
    'none': 0,
    'not applicable': -1
}

security_capabilities = [
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Are you accounting for OWASP top 10 Critical Vuln flaws?", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Documented Security Requirements", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Documented Security Test Cases", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Dynamic appsec testing", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Manual Code Review", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS,
     "Patterns & Reference Architecture documented for Security Features", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Pen testing", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Prior to Packaging, Vuln/Malware/Anti-Virus scanning", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Risk Assessment & Business Impact Analysis", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Secure Coding Guide", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Security Architecture", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Security Awareness Training", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Security Test Plan", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Static Code Analysis", ""],
    [scoring.PROCESS, SEC_SFTWR_MNGMNT_LFCYCL_GDLNS, "Threat Model", ""],
    [scoring.PROCESS, SECURITY_EXCEPTION_RISK, "Overall Risk Score", "http://prodsec.redhat.com/static/supported.html"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES,
     "All Logs Use Common Logging and Can Be Sent Externally, Encrypted", ""],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Cryptographic Agility without Recompiling", ""],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Has a Known FirewallD Configuration", "AC-17(9), SC-7(12)"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES,
     "Instructions Exist to Enable SSL/TLS or Is Enabled by Default", "AC-17(2), CM-7"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Supports Attestation with SCAP", "CM-6"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Supports Auditing Security Events",
     "AC-17(7), AU-1(b), AU-2(a), AU-2(c), AU-2(d), AU-2(4), AU-6(9), AU-12(a), AU-12(c), IR-5"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Supports Centralized Logging", "AU-6, AU-3(2), SI-4(2)"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Supports Identity Management", ""],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Supports Kerberos Based SSO", ""],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Works with FIPS Enabled", "AC-17(2)"],
    [scoring.TECHNOLOGY, SECURITY_CAPABILITIES, "Works with SELINUX Set to Enforcing",
     "AC-3, AC-3(3), AC-3(4), AC-4, AC-6, AU-9, SI-6(a), SC-7(12)"],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "C2S Benchmarks", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "Common Criteria", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "FIPS 140-2", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "FedRAMP", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "HIPAA", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "ISO 27001:2013", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "NIST 800-53", ""],
    [scoring.COMPLIANCE, COMPLIANCE_FRAMEWORK_COLLATERAL, "PCI-DSSv3", ""]
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
