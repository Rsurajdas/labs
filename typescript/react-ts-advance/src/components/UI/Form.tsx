import {
  type ComponentPropsWithoutRef,
  type ReactNode,
  type SubmitEvent,
  forwardRef,
  useRef,
  useImperativeHandle,
} from "react";

export interface FormHandleRef {
  clear: () => void;
}

interface FormProps extends ComponentPropsWithoutRef<"form"> {
  onSave: (data: unknown) => void;
  children: ReactNode;
}

const Form = forwardRef<FormHandleRef, FormProps>(function (
  { onSave, children, ...props }: FormProps,
  ref,
) {
  const formRef = useRef<HTMLFormElement>(null);
  useImperativeHandle(ref, () => {
    return {
      clear: () => {
        formRef.current?.reset();
      },
    };
  });
  const handleSubmit = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());
    onSave(data);
  };
  return (
    <form onSubmit={handleSubmit} {...props} ref={formRef}>
      {children}
    </form>
  );
});

export default Form;
