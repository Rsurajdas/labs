interface InputsProps {
  label: string;
  id: string;
}

export default function Inputs({ label, id }: InputsProps) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input name={id} type="text" />
    </div>
  );
}
