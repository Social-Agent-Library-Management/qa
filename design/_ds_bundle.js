/* @ds-bundle: {"format":4,"namespace":"DesignSystem_307f43","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"DataTable","sourcePath":"components/data/DataTable.jsx"},{"name":"DdayCard","sourcePath":"components/display/DdayCard.jsx"},{"name":"StatCard","sourcePath":"components/display/StatCard.jsx"},{"name":"SIDEBAR_NAV_ITEMS","sourcePath":"components/navigation/Sidebar.jsx"},{"name":"ADMIN_NAV_ITEMS","sourcePath":"components/navigation/Sidebar.jsx"},{"name":"Sidebar","sourcePath":"components/navigation/Sidebar.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"957f3e59cf1b","components/core/Button.jsx":"75c32aacd4a9","components/core/Card.jsx":"85ef8c986fb7","components/core/Input.jsx":"7c9389ce4250","components/data/DataTable.jsx":"ee72ae070171","components/display/DdayCard.jsx":"714fd6327ab4","components/display/StatCard.jsx":"5b64ca7319e2","components/navigation/Sidebar.jsx":"6eead6b82fac"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.DesignSystem_307f43 = window.DesignSystem_307f43 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
const STATUS_CONFIG = {
  available: {
    label: '대출가능',
    background: 'var(--color-success-light)',
    color: 'var(--color-success)'
  },
  loaned: {
    label: '대출중',
    background: '#FFF0D6',
    color: 'var(--color-warning)'
  },
  overdue: {
    label: '연체',
    background: 'var(--color-danger-light)',
    color: 'var(--color-danger)'
  },
  returned: {
    label: '반납완료',
    background: 'var(--color-bg)',
    color: 'var(--color-text-secondary)'
  },
  lost: {
    label: '분실',
    background: 'var(--color-danger-light)',
    color: 'var(--color-danger)'
  },
  disposed: {
    label: '폐기',
    background: 'var(--color-bg)',
    color: 'var(--color-text-placeholder)'
  },
  copy: {
    label: '소장본',
    background: 'var(--color-copy-light)',
    color: 'var(--color-copy)'
  }
};
const SIZES = {
  sm: {
    fontSize: 10,
    paddingX: 7,
    height: 18
  },
  md: {
    fontSize: 11,
    paddingX: 10,
    height: 22
  },
  lg: {
    fontSize: 13,
    paddingX: 12,
    height: 26
  }
};
function Badge({
  status = 'available',
  label,
  size = 'md'
}) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.available;
  const s = SIZES[size] || SIZES.md;
  const displayLabel = label !== undefined ? label : config.label;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: config.background,
      color: config.color,
      fontSize: s.fontSize,
      fontWeight: 'var(--font-weight-medium)',
      fontFamily: 'var(--font-family-base)',
      padding: `0 ${s.paddingX}px`,
      height: s.height,
      borderRadius: 'var(--radius-badge)',
      letterSpacing: 'var(--letter-spacing-normal)',
      whiteSpace: 'nowrap',
      lineHeight: 1,
      flexShrink: 0
    }
  }, displayLabel);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
const VARIANTS = {
  primary: {
    background: 'var(--color-primary)',
    color: '#fff',
    border: 'none',
    hoverBg: 'var(--color-primary-hover)'
  },
  secondary: {
    background: 'var(--color-surface)',
    color: 'var(--color-primary)',
    border: '1.5px solid var(--color-primary)',
    hoverBg: 'var(--color-primary-light)'
  },
  ghost: {
    background: 'transparent',
    color: 'var(--color-text-primary)',
    border: '1px solid var(--color-border)',
    hoverBg: 'var(--color-surface-secondary)'
  },
  danger: {
    background: 'var(--color-danger)',
    color: '#fff',
    border: 'none',
    hoverBg: '#D93025'
  },
  success: {
    background: 'var(--color-success)',
    color: '#fff',
    border: 'none',
    hoverBg: '#28A745'
  }
};
const SIZES = {
  sm: {
    fontSize: 'var(--font-size-sm)',
    height: 30,
    paddingX: 12,
    gap: 4
  },
  md: {
    fontSize: 'var(--font-size-body)',
    height: 40,
    paddingX: 18,
    gap: 6
  },
  lg: {
    fontSize: 'var(--font-size-lg)',
    height: 48,
    paddingX: 24,
    gap: 8
  }
};
function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  fullWidth = false,
  onClick,
  type = 'button',
  icon
}) {
  const [hovered, setHovered] = React.useState(false);
  const [pressed, setPressed] = React.useState(false);
  const v = VARIANTS[variant] || VARIANTS.primary;
  const s = SIZES[size] || SIZES.md;
  return /*#__PURE__*/React.createElement("button", {
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => !disabled && setHovered(true),
    onMouseLeave: () => {
      setHovered(false);
      setPressed(false);
    },
    onMouseDown: () => !disabled && setPressed(true),
    onMouseUp: () => setPressed(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: s.gap,
      height: s.height,
      padding: `0 ${s.paddingX}px`,
      fontSize: s.fontSize,
      fontFamily: 'var(--font-family-base)',
      fontWeight: 'var(--font-weight-semibold)',
      letterSpacing: 'var(--letter-spacing-normal)',
      borderRadius: 'var(--radius-button)',
      border: v.border || 'none',
      background: hovered && !disabled ? v.hoverBg : v.background,
      color: v.color,
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.42 : 1,
      width: fullWidth ? '100%' : undefined,
      transform: pressed && !disabled ? 'scale(0.97)' : 'none',
      transition: 'background 0.12s ease, opacity 0.12s ease, transform 0.08s ease',
      outline: 'none',
      whiteSpace: 'nowrap',
      lineHeight: 1,
      boxSizing: 'border-box',
      textDecoration: 'none'
    }
  }, icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      flexShrink: 0
    }
  }, icon), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
const PADDING_MAP = {
  sm: 16,
  md: 24,
  lg: 32
};
function Card({
  children,
  title,
  titleRight,
  padding = 'md',
  noPadding = false,
  style
}) {
  const p = PADDING_MAP[padding] ?? 24;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--color-surface)',
      borderRadius: 'var(--radius-card)',
      overflow: 'hidden',
      ...style
    }
  }, title && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: `20px ${p}px 16px`,
      borderBottom: '1px solid var(--color-border)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--font-size-xl)',
      fontWeight: 'var(--font-weight-semibold)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-tight)',
      lineHeight: 1.3
    }
  }, title), titleRight !== undefined && /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0
    }
  }, titleRight)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: noPadding ? 0 : title ? `16px ${p}px ${p}px` : p
    }
  }, children));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
let _idCounter = 0;
function Input({
  label,
  placeholder = '',
  required = false,
  value,
  onChange,
  type = 'text',
  disabled = false,
  hint,
  error,
  id
}) {
  const [focused, setFocused] = React.useState(false);
  const inputId = React.useMemo(() => id || `input-${++_idCounter}`, [id]);
  const borderColor = error ? 'var(--color-danger)' : focused ? 'var(--color-primary)' : 'var(--color-border)';
  const boxShadow = focused && !error ? '0 0 0 3px rgba(0,122,255,0.12)' : 'none';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6,
      width: '100%'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontSize: 'var(--font-size-base)',
      fontWeight: 'var(--font-weight-semibold)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      lineHeight: 1.4
    }
  }, label, required && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--color-danger)',
      marginLeft: 2
    }
  }, "*")), /*#__PURE__*/React.createElement("input", {
    id: inputId,
    type: type,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: {
      width: '100%',
      height: 44,
      padding: `0 var(--space-input-x)`,
      fontSize: 'var(--font-size-body)',
      fontFamily: 'var(--font-family-base)',
      fontWeight: 'var(--font-weight-regular)',
      color: 'var(--color-text-primary)',
      background: disabled ? 'var(--color-surface-secondary)' : 'var(--color-surface)',
      border: `1px solid ${borderColor}`,
      borderRadius: 'var(--radius-input)',
      outline: 'none',
      boxSizing: 'border-box',
      boxShadow,
      transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
      cursor: disabled ? 'not-allowed' : 'text',
      opacity: disabled ? 0.55 : 1
    }
  }), hint && !error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--font-size-sm)',
      color: 'var(--color-text-secondary)',
      fontFamily: 'var(--font-family-base)',
      lineHeight: 1.4
    }
  }, hint), error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--font-size-sm)',
      color: 'var(--color-danger)',
      fontFamily: 'var(--font-family-base)',
      lineHeight: 1.4
    }
  }, error));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/data/DataTable.jsx
try { (() => {
function DataTable({
  columns = [],
  rows = [],
  renderCell,
  emptyText = '데이터가 없습니다.',
  onRowClick,
  pageSize
}) {
  const [hoveredRow, setHoveredRow] = React.useState(null);
  const [page, setPage] = React.useState(1);
  const paginated = typeof pageSize === 'number' && pageSize > 0;
  const total = rows.length;
  const totalPages = paginated ? Math.max(1, Math.ceil(total / pageSize)) : 1;
  const current = Math.min(page, totalPages);
  React.useEffect(() => {
    setPage(1);
  }, [total, pageSize]);
  const start = paginated ? (current - 1) * pageSize : 0;
  const visibleRows = paginated ? rows.slice(start, start + pageSize) : rows;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      overflowX: 'auto'
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      borderCollapse: 'collapse',
      fontFamily: 'var(--font-family-base)',
      tableLayout: 'auto'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: 'var(--color-surface-secondary)',
      borderTop: '1px solid var(--color-border)',
      borderBottom: '1px solid var(--color-border)'
    }
  }, columns.map(col => /*#__PURE__*/React.createElement("th", {
    key: col.key,
    style: {
      padding: '10px 16px',
      textAlign: 'left',
      fontSize: 'var(--font-size-sm)',
      fontWeight: 'var(--font-weight-semibold)',
      color: 'var(--color-text-secondary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      width: col.width,
      whiteSpace: 'nowrap',
      fontFamily: 'var(--font-family-base)'
    }
  }, col.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.length === 0 ? /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    colSpan: columns.length,
    style: {
      textAlign: 'center',
      padding: '48px 16px',
      color: 'var(--color-text-secondary)',
      fontSize: 'var(--font-size-body)',
      fontFamily: 'var(--font-family-base)'
    }
  }, emptyText)) : visibleRows.map((row, i) => /*#__PURE__*/React.createElement("tr", {
    key: i,
    onClick: () => onRowClick && onRowClick(row, i),
    onMouseEnter: () => setHoveredRow(i),
    onMouseLeave: () => setHoveredRow(null),
    style: {
      background: hoveredRow === i ? 'var(--color-surface-secondary)' : 'transparent',
      borderBottom: `1px solid var(--color-bg)`,
      cursor: onRowClick ? 'pointer' : 'default',
      transition: 'background 0.1s ease'
    }
  }, columns.map(col => /*#__PURE__*/React.createElement("td", {
    key: col.key,
    style: {
      padding: '14px 16px',
      fontSize: 'var(--font-size-md)',
      color: col.secondary ? 'var(--color-text-secondary)' : 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      verticalAlign: 'middle',
      fontFamily: 'var(--font-family-base)',
      lineHeight: 1.4,
      whiteSpace: col.nowrap ? 'nowrap' : 'normal'
    }
  }, renderCell ? renderCell(col, row[col.key], row) : row[col.key]))))))), paginated && total > 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 16,
      padding: '12px 16px',
      borderTop: '1px solid var(--color-border)',
      fontFamily: 'var(--font-family-base)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-sm)',
      color: 'var(--color-text-secondary)',
      whiteSpace: 'nowrap'
    }
  }, "\uCD1D ", total.toLocaleString(), "\uAC74 \uC911 ", (start + 1).toLocaleString(), "\u2013", Math.min(start + pageSize, total).toLocaleString()), totalPages > 1 && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 4
    }
  }, /*#__PURE__*/React.createElement(PageButton, {
    disabled: current === 1,
    onClick: () => setPage(current - 1)
  }, "\uC774\uC804"), pageNumbers(current, totalPages).map((p, i) => p === '…' ? /*#__PURE__*/React.createElement("span", {
    key: `gap${i}`,
    style: {
      padding: '0 4px',
      fontSize: 'var(--font-size-sm)',
      color: 'var(--color-text-placeholder)'
    }
  }, "\u2026") : /*#__PURE__*/React.createElement(PageButton, {
    key: p,
    active: p === current,
    onClick: () => setPage(p)
  }, p)), /*#__PURE__*/React.createElement(PageButton, {
    disabled: current === totalPages,
    onClick: () => setPage(current + 1)
  }, "\uB2E4\uC74C"))));
}
function pageNumbers(current, totalPages) {
  if (totalPages <= 7) return Array.from({
    length: totalPages
  }, (_, i) => i + 1);
  const out = [1];
  const from = Math.max(2, current - 1);
  const to = Math.min(totalPages - 1, current + 1);
  if (from > 2) out.push('…');
  for (let p = from; p <= to; p++) out.push(p);
  if (to < totalPages - 1) out.push('…');
  out.push(totalPages);
  return out;
}
function PageButton({
  children,
  active,
  disabled,
  onClick
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClick,
    disabled: disabled,
    style: {
      minWidth: 30,
      height: 30,
      padding: '0 9px',
      borderRadius: 'var(--radius-sm, 6px)',
      border: `1px solid ${active ? 'var(--color-primary)' : 'var(--color-border)'}`,
      background: active ? 'var(--color-primary)' : 'var(--color-surface)',
      color: active ? '#FFFFFF' : disabled ? 'var(--color-text-placeholder)' : 'var(--color-text-primary)',
      fontSize: 'var(--font-size-sm)',
      fontWeight: active ? 'var(--font-weight-semibold)' : 'var(--font-weight-regular)',
      fontFamily: 'var(--font-family-base)',
      letterSpacing: 'var(--letter-spacing-normal)',
      cursor: disabled ? 'default' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      lineHeight: 1
    }
  }, children);
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/DataTable.jsx", error: String((e && e.message) || e) }); }

// components/display/DdayCard.jsx
try { (() => {
function getUrgency(daysLeft) {
  if (daysLeft <= 0) return 'urgent';
  if (daysLeft <= 2) return 'urgent';
  if (daysLeft <= 5) return 'warning';
  return 'normal';
}
const URGENCY = {
  urgent: {
    bg: 'var(--color-urgent-bg)',
    iconBg: 'var(--color-danger-light)',
    iconColor: 'var(--color-danger)',
    badgeBg: 'var(--color-danger)'
  },
  warning: {
    bg: 'var(--color-warning-bg)',
    iconBg: 'var(--color-warning-light)',
    iconColor: 'var(--color-warning)',
    badgeBg: 'var(--color-warning)'
  },
  normal: {
    bg: 'var(--color-normal-bg)',
    iconBg: 'var(--color-border)',
    iconColor: 'var(--color-text-secondary)',
    badgeBg: 'var(--color-text-secondary)'
  }
};
function DdayCard({
  title,
  meta,
  daysLeft
}) {
  const urgency = getUrgency(daysLeft);
  const s = URGENCY[urgency];
  const dLabel = daysLeft < 0 ? `D+${Math.abs(daysLeft)}` : daysLeft === 0 ? 'D-Day' : `D-${daysLeft}`;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      background: s.bg,
      borderRadius: 'var(--radius-dday)',
      padding: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 40,
      height: 40,
      borderRadius: 'var(--radius-dday)',
      background: s.iconBg,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "3",
    width: "16",
    height: "15",
    rx: "2",
    stroke: s.iconColor,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 1v4M14 1v4",
    stroke: s.iconColor,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M2 8h16",
    stroke: s.iconColor,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M5 12h4M5 15h3",
    stroke: s.iconColor,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-md)',
      fontWeight: 'var(--font-weight-medium)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      marginBottom: 3
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-base)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-secondary)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      lineHeight: 1.4
    }
  }, meta)), /*#__PURE__*/React.createElement("div", {
    style: {
      background: s.badgeBg,
      color: '#fff',
      fontSize: 'var(--font-size-base)',
      fontWeight: 'var(--font-weight-semibold)',
      fontFamily: 'var(--font-family-base)',
      padding: '5px 14px',
      borderRadius: 'var(--radius-badge)',
      flexShrink: 0,
      minWidth: 52,
      textAlign: 'center',
      letterSpacing: 'var(--letter-spacing-normal)',
      lineHeight: 1
    }
  }, dLabel));
}
Object.assign(__ds_scope, { DdayCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/DdayCard.jsx", error: String((e && e.message) || e) }); }

// components/display/StatCard.jsx
try { (() => {
function StatCard({
  label,
  value,
  sub,
  subColor,
  iconBg = 'var(--color-primary-light)',
  icon
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 16,
      background: 'var(--color-surface)',
      borderRadius: 'var(--radius-card)',
      padding: '20px 24px',
      minWidth: 0,
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 48,
      height: 48,
      borderRadius: '50%',
      background: iconBg,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, icon), /*#__PURE__*/React.createElement("div", {
    style: {
      minWidth: 0,
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-base)',
      fontWeight: 'var(--font-weight-regular)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-secondary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      marginBottom: 4,
      lineHeight: 1.3,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-3xl)',
      fontWeight: 'var(--font-weight-bold)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-tight)',
      lineHeight: 1
    }
  }, value), sub && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-sm)',
      fontFamily: 'var(--font-family-base)',
      color: subColor || 'var(--color-text-secondary)',
      marginTop: 5,
      lineHeight: 1.3,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, sub)));
}
Object.assign(__ds_scope, { StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/StatCard.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Sidebar.jsx
try { (() => {
/* ── Built-in icon set ─────────────────────────────────────────────── */
function IconDashboard({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "2",
    width: "7",
    height: "8",
    rx: "1.5",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "11",
    y: "2",
    width: "7",
    height: "5",
    rx: "1.5",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "13",
    width: "7",
    height: "5",
    rx: "1.5",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "11",
    y: "10",
    width: "7",
    height: "8",
    rx: "1.5",
    stroke: color,
    strokeWidth: "1.5"
  }));
}
function IconBook({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 3h10v14H4z",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 3v14",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 7h4M6 10h4",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconCopy({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "5",
    width: "12",
    height: "13",
    rx: "1.5",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 2h10a1.5 1.5 0 0 1 1.5 1.5V16",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconLoan({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 17V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M2 17h16",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 8h4M8 11h4",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconReturn({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 10a6 6 0 1 1 1.5 4",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 14v-4h4",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }));
}
function IconHistory({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "10",
    cy: "10",
    r: "7",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 6v4l3 2",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }));
}
function IconSearch({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "9",
    cy: "9",
    r: "6",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M13.5 13.5L17 17",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconImport({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M10 3v8m0 0L7 8m3 3l3-3",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 13v2a1 1 0 001 1h10a1 1 0 001-1v-2",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconExport({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M10 12V4m0 0L7 7m3-3l3 3",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 13v2a1 1 0 001 1h10a1 1 0 001-1v-2",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconAdmin({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "20",
    height: "20",
    viewBox: "0 0 20 20",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "10",
    cy: "10",
    r: "2.5",
    stroke: color,
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 2.5v2M10 15.5v2M17.5 10h-2M4.5 10h-2M15.3 4.7l-1.4 1.4M6.1 13.9l-1.4 1.4M15.3 15.3l-1.4-1.4M6.1 6.1L4.7 4.7",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }));
}
function IconLogout({
  color
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M10 3h3a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-3",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M7 5l-3 3 3 3M4 8h8",
    stroke: color,
    strokeWidth: "1.5",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }));
}

/* Primary nav — day-to-day volunteer tasks. Admin-only screens live behind the 관리자 페이지 hub. */
const SIDEBAR_NAV_ITEMS = [{
  id: 'dashboard',
  label: '대시보드',
  Icon: IconDashboard
}, {
  id: 'book-search',
  label: '도서 검색',
  Icon: IconSearch
}, {
  id: 'loan-register',
  label: '대출 등록',
  Icon: IconLoan
}, {
  id: 'return',
  label: '반납 처리',
  Icon: IconReturn
}, {
  id: 'admin',
  label: '관리자 페이지',
  Icon: IconAdmin
}];

/* Sub-pages shown inside the 관리자 페이지 hub. */
const ADMIN_NAV_ITEMS = [{
  id: 'book-register',
  label: '도서 등록',
  desc: 'ISBN 조회로 새 도서를 등록합니다.',
  Icon: IconBook
}, {
  id: 'copy-register',
  label: '소장본 등록',
  desc: '등록된 도서의 실물 소장본을 추가합니다.',
  Icon: IconCopy
}, {
  id: 'loan-history',
  label: '대출 내역 조회',
  desc: '전체 대출·반납 이력을 조회합니다.',
  Icon: IconHistory
}, {
  id: 'excel-import',
  label: '엑셀 일괄 등록',
  desc: '엑셀 파일로 도서를 한 번에 등록합니다.',
  Icon: IconImport
}, {
  id: 'data-export',
  label: '내보내기',
  desc: '데이터를 엑셀/CSV로 내려받습니다.',
  Icon: IconExport
}];
function Sidebar({
  items,
  activeId = 'dashboard',
  onSelect,
  user = {
    name: '관리자',
    email: 'admin@library.go.kr'
  },
  onLogout
}) {
  const navItems = items || SIDEBAR_NAV_ITEMS;
  const [hoveredId, setHoveredId] = React.useState(null);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: 260,
      minWidth: 260,
      height: '100%',
      background: 'var(--color-surface)',
      borderRight: '1px solid var(--color-border)',
      display: 'flex',
      flexDirection: 'column',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 72,
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '0 20px',
      borderBottom: '1px solid var(--color-border)',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 40,
      height: 40,
      borderRadius: 'var(--radius-logo)',
      background: 'var(--color-primary)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "22",
    height: "22",
    viewBox: "0 0 22 22",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 5h14M4 9h14M4 13h10M4 17h14",
    stroke: "white",
    strokeWidth: "2",
    strokeLinecap: "round"
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--font-size-lg)',
      fontWeight: 'var(--font-weight-bold)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-tight)',
      lineHeight: 1.2
    }
  }, "\uB3C4\uC11C \uAD00\uB9AC \uC2DC\uC2A4\uD15C")), /*#__PURE__*/React.createElement("nav", {
    style: {
      flex: 1,
      padding: '8px 8px',
      overflowY: 'auto'
    }
  }, navItems.map(item => {
    const isActive = item.id === activeId;
    const isHovered = item.id === hoveredId && !isActive;
    const iconColor = isActive ? 'var(--color-primary)' : 'var(--color-text-secondary)';
    return /*#__PURE__*/React.createElement("button", {
      key: item.id,
      onClick: () => onSelect && onSelect(item.id),
      onMouseEnter: () => setHoveredId(item.id),
      onMouseLeave: () => setHoveredId(null),
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        width: '100%',
        height: 44,
        padding: '0 16px',
        borderRadius: 8,
        border: 'none',
        background: isActive ? 'var(--color-primary-light)' : isHovered ? 'var(--color-bg)' : 'transparent',
        cursor: 'pointer',
        marginBottom: 2,
        transition: 'background 0.1s ease',
        outline: 'none'
      }
    }, item.Icon && /*#__PURE__*/React.createElement(item.Icon, {
      color: iconColor
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 'var(--font-size-body)',
        fontWeight: isActive ? 'var(--font-weight-semibold)' : 'var(--font-weight-regular)',
        fontFamily: 'var(--font-family-base)',
        color: isActive ? 'var(--color-primary)' : 'var(--color-text-primary)',
        letterSpacing: 'var(--letter-spacing-normal)',
        lineHeight: 1
      }
    }, item.label));
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: '1px solid var(--color-border)',
      padding: '14px 20px',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 36,
      height: 36,
      borderRadius: '50%',
      background: 'var(--color-border)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
      fontSize: 14,
      fontWeight: 600,
      color: 'var(--color-text-secondary)',
      fontFamily: 'var(--font-family-base)'
    }
  }, "\uAD00"), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-md)',
      fontWeight: 'var(--font-weight-semibold)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-primary)',
      letterSpacing: 'var(--letter-spacing-normal)',
      lineHeight: 1.3
    }
  }, user.name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--font-size-sm)',
      fontFamily: 'var(--font-family-base)',
      color: 'var(--color-text-secondary)',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      lineHeight: 1.4
    }
  }, user.email)), onLogout && /*#__PURE__*/React.createElement("button", {
    onClick: onLogout,
    style: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      padding: 4,
      display: 'flex',
      alignItems: 'center',
      borderRadius: 4,
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(IconLogout, {
    color: "var(--color-text-secondary)"
  }))));
}
Object.assign(__ds_scope, { SIDEBAR_NAV_ITEMS, ADMIN_NAV_ITEMS, Sidebar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Sidebar.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.DataTable = __ds_scope.DataTable;

__ds_ns.DdayCard = __ds_scope.DdayCard;

__ds_ns.StatCard = __ds_scope.StatCard;

__ds_ns.SIDEBAR_NAV_ITEMS = __ds_scope.SIDEBAR_NAV_ITEMS;

__ds_ns.ADMIN_NAV_ITEMS = __ds_scope.ADMIN_NAV_ITEMS;

__ds_ns.Sidebar = __ds_scope.Sidebar;

})();
