dict_1 = [
    ('name', '1'),
    ('vendor', '2'),
    ('production_site', '4'),
    ('applicant', '5'),
    ('reg_item_number', '7'),
    ('reg_date', '8'),
    ('validity', '9',)
]

dict_2 = [
    ('manufacturing_company', '3'),
    ('certificates_no', '6'),
]

request_data = {
    'QueryStringFind': 'Rk9wdC5WQW5bPV1GYWxzZVs7XUZPcHQuVlVuVGVybVs9XUZhbHNlWztdRk9wdC5WUGF1c2VbPV1GYWxzZVs7XUZPcHQuVkZpbGVzWz1dVHJ1ZVs7XUZPcHQuVkVGaWVsZDFbPV1GYWxzZVs7XUZPcHQuT3JkZXJCeVs9XVByb2R1Y3ROYW1lWztdRk9wdC5EaXJPcmRlcls9XWFzY1s7XUZPcHQuVlRbPV10WztdRk9wdC5QYWdlQ1s9XTEwMFs7XUZPcHQuUGFnZU5bPV0xWztdRk9wdC5DUmVjWz1dMTk3NzZbO11GT3B0LkNQYWdlWz1dMTk4WztdRlByb3BzWzBdLk5hbWVbPV1Qcm9kdWN0TmFtZVs7XUZQcm9wc1swXS5Jc1RleHRbPV1UcnVlWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5WYWxbPV0gWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5FeGNsWz1dRmFsc2VbO11GUHJvcHNbMF0uQ3JpdEVsZW1zWzBdLkNyaXRbPV1MaWtlWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5OdW1bPV0xWztdRlByb3BzWzFdLk5hbWVbPV1UeXBlWztdRlByb3BzWzFdLklzRHJvcFs9XVRydWVbO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLlZhbFs9XV9bO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLkV4Y2xbPV1GYWxzZVs7XUZQcm9wc1sxXS5Dcml0RWxlbXNbMF0uQ3JpdFs9XUxpa2VbO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLk51bVs9XTFbO11GUHJvcHNbMl0uTmFtZVs9XU1hbnVmYWN0dXJlcls7XUZQcm9wc1syXS5Jc1RleHRbPV1UcnVlWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5WYWxbPV1fWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5FeGNsWz1dRmFsc2VbO11GUHJvcHNbMl0uQ3JpdEVsZW1zWzBdLkNyaXRbPV1MaWtlWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5OdW1bPV0xWztdRlByb3BzWzNdLk5hbWVbPV1EZWNsYXJhbnRbO11GUHJvcHNbM10uSXNUZXh0Wz1dVHJ1ZVs7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uVmFsWz1dX1s7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uRXhjbFs9XUZhbHNlWztdRlByb3BzWzNdLkNyaXRFbGVtc1swXS5Dcml0Wz1dTGlrZVs7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uTnVtWz1dMVs7XUZQcm9wc1s0XS5OYW1lWz1dQ2VydGlmaWNhdGVOdW1iZXJbO11GUHJvcHNbNF0uSXNUZXh0Wz1dVHJ1ZVs7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uVmFsWz1dX1s7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uRXhjbFs9XUZhbHNlWztdRlByb3BzWzRdLkNyaXRFbGVtc1swXS5Dcml0Wz1dTGlrZVs7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uTnVtWz1dMVs7XUZQcm9wc1s1XS5OYW1lWz1dQ2VydGlmaWNhdGVEYXRlWztdRlByb3BzWzVdLklzRGF0ZVs9XVRydWVbO11GUHJvcHNbNV0uQ3JpdEVsZW1zRC5WYWwxWz1dbnVsbFs7XUZQcm9wc1s1XS5Dcml0RWxlbXNELlZhbDJbPV1udWxsWztdRlByb3BzWzVdLkNyaXRFbGVtc0QuQ3JpdFs9XUVxdWFsWztdRlByb3BzWzZdLk5hbWVbPV1UZXJtWztdRlByb3BzWzZdLklzRGF0ZVs9XVRydWVbO11GUHJvcHNbNl0uQ3JpdEVsZW1zRC5WYWwxWz1dbnVsbFs7XUZQcm9wc1s2XS5Dcml0RWxlbXNELlZhbDJbPV1udWxsWztdRlByb3BzWzZdLkNyaXRFbGVtc0QuQ3JpdFs9XUVxdWFsWztd',
    'IsPostBack': 'True',
    'PropSubmit': 'FOpt_PageN',
    'VFiles': 'True',
    'FProps[0].IsText': 'True',
    'FProps[0].Name': 'ProductName',
    'FProps[0].CritElems[0].Num': '1',
    'FProps[0].CritElems[0].Val':  ' ',
    'FProps[0].CritElems[0].Crit': 'Like',
    'FProps[0].CritElems[0].Excl': 'false',
    'FProps[1].IsDrop': 'True',
    'FProps[1].Name': 'Type',
    'FProps[1].CritElems[0].Num': '1',
    'FProps[1].CritElems[0].Val': '',
    'FProps[1].CritElems[0].Excl': 'false',
    'FProps[2].IsText': 'True',
    'FProps[2].Name': 'Manufacturer',
    'FProps[2].CritElems[0].Num': '1',
    'FProps[2].CritElems[0].Val': '',
    'FProps[2].CritElems[0].Crit': 'Like',
    'FProps[2].CritElems[0].Excl': 'false',
    'FProps[3].IsText': 'True',
    'FProps[3].Name': 'Declarant',
    'FProps[3].CritElems[0].Num': '1',
    'FProps[3].CritElems[0].Val': '',
    'FProps[3].CritElems[0].Crit': 'Like',
    'FProps[3].CritElems[0].Excl': 'false',
    'FProps[4].IsText': 'True',
    'FProps[4].Name': 'CertificateNumber',
    'FProps[4].CritElems[0].Num': '1',
    'FProps[4].CritElems[0].Val': '',
    'FProps[4].CritElems[0].Crit': 'Like',
    'FProps[4].CritElems[0].Excl': 'false',
    'FProps[5].IsDate': 'True',
    'FProps[5].Name': 'CertificateDate',
    'FProps[5].CritElemsD.Val1': '',
    'FProps[5].CritElemsD.Crit': 'Equal',
    'FProps[6].IsDate': 'True',
    'FProps[6].Name': 'Term',
    'FProps[6].CritElemsD.Val1': '',
    'FProps[6].CritElemsD.Crit': 'Equal',
    'FOpt.PageC': '100',
    'FOpt.OrderBy': 'ProductName',
    'FOpt.DirOrder': 'asc',
    'FOpt.VFiles': 'true',
    'FOpt.VFiles': 'false',
    }