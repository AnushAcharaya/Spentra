const Table = ({ columns, data }) => (
  <div className="overflow-x-auto">
    <table className="min-w-full bg-white border border-gray-200 rounded">
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.accessor} className="px-4 py-2 border-b bg-spentra-100 text-left text-spentra-700 font-semibold">
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data && data.length > 0 ? (
          data.map((row, i) => (
            <tr key={i} className="hover:bg-spentra-50">
              {columns.map(col => (
                <td key={col.accessor} className="px-4 py-2 border-b">
                  {row[col.accessor]}
                </td>
              ))}
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan={columns.length} className="px-4 py-4 text-center text-gray-400">No data</td>
          </tr>
        )}
      </tbody>
    </table>
  </div>
);

export default Table; 