import { useState } from 'react';
import Image from 'next/image';
import cx from "classnames";

// components
import ImageBtn from 'components/imageBtn';

// styles
import StyleCSS from "./style.module.css";

// icons
import CompanyIcon from "icons/company.png";
import DiggerIcon from 'icons/digger.png';
import ForwardIcon from 'icons/forward.png';
import BackwardIcon from 'icons/backward.png';


const Index = () => {
  const [isOpen, setIsOpen] = useState(false)

  const toggleOpen = () => {
    let isOpenClone = isOpen
    setIsOpen(!isOpenClone)
  }

  const style = () => {
    if (isOpen) {
      return cx('grid col-span-5', StyleCSS.expanded)
    } else {
      return 'grid grid-cols-1 justify-items-center'
    }
  }

  const showNavWords = () => {
    if (isOpen) {
      return "flex justify-items-center"
    } else {
      return ""
    }
  }

  return (
    <div className={cx(StyleCSS.main, 'md:hidden', style())}>

      <div className='flex'>
        {
          isOpen ?
            <div className='flex w-full'>
              <div className='flex w-full justify-evenly gap-3'>
                <div>
                  <ImageBtn
                    img={CompanyIcon}
                    width={50}
                    height={50}
                    action={{
                      url:'/about'
                    }}
                  />
                  <span>About Us</span>
                </div>
                <div>
                  <ImageBtn
                    img={DiggerIcon}
                    width={50}
                    height={50}
                    action={{
                      url:'/contactus'
                    }}
                  />
                  <span>Services</span>
                </div>
              </div>
              <Image
                src={ForwardIcon}
                width={50}
                height={50}
                onClick={toggleOpen}
              />
            </div>
            :

          <div className='flex flex-col gap-3'>
            <ImageBtn
                img={CompanyIcon}
                width={50}
                height={50}
                action={{
                  url:'/about'
                }}
                />
                <ImageBtn
                img={DiggerIcon}
                width={50}
                height={50}
                action={{
                  url:'/contactus'
                }}
                />
            <Image
            src={BackwardIcon}
            width={50}
            height={50}
            onClick={toggleOpen}
            />
          </div>
        }
      </div>
    </div>
  );
}

export default Index;