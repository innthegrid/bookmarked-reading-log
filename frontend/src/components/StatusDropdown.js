/* frontend/src/components/StatusDropdown.js */
export default function StatusDropdown({ status, onChange }) {

  return (
    <div className="nes-select">
      <select value={status} onChange={(e)=>onChange(e.target.value)}>
        <option value="">Add to Library</option>
        <option value="want_to_read">
          To Read
        </option>
        <option value="reading">
          Reading
        </option>
        <option value="completed">
          Completed
        </option>
      </select>
    </div>
  );
}